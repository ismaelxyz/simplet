#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2020 Ismael Belisario

# This file is part of Open Translation.

# Open Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Open Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Open Translation. If not, see <https://www.gnu.org/licenses/>.


# Script Name: combobox.py


from tkinter.ttk import Combobox, Label, Frame
from random import choice


class OTACombobox(Combobox):
    """
        Name: Open Translation Autocomplete Combobox
        Autocomplete text in this combobox
    """

    def __init__(self, master, completevalues=None, sync=False, **kwargs):
        
        """
        Create an AutocompleteCombobox.

        :param master: master widget
        :type master: widget
        :param completevalues: autocompletion values
        :type completevalues: list
        :param kwargs: keyword arguments passed to the :class:`Combobox` initializer
        """

        self.__text = ''
        super().__init__(master, values=completevalues, **kwargs)
        self._completion_list = completevalues
       
        if isinstance(completevalues, list):
            self.set_completion_list(completevalues)

        self._hits = []
        self._hit_index = 0
        self.position = 0
        
        self.bind('<Enter>', self._save_text)
        self.bind('<Leave>', self._comfirm_text)
        
        # self.bind('<Key-Return>', self._comfirm_text)

        self.bind('<FocusIn>', self._save_text)
        self.bind('<FocusOut>', self._comfirm_text)
        
        self.sync_v = sync
        #print(self.keys())
            #exit()
            
    @property
    def view_text(self):
        return self.__text
    
    def _save_text(self, even):
        if self.__text == '':  # Control of input (very binds; create conflict).
            self.__text = self.get()
    
    def _comfirm_text(self, even):
        
        if self.get() not in list(self.values):
            self.delete(0, 'end')
            self.set(self.__text)
            self.__text = ''
            self.icursor('end')
            return True
        
        if self.sync_v:
            self.__sync()
            self.icursor('end')
        self.__text = ''
        return False

    def set_completion_list(self, completion_list):
        """
        Use the completion list as drop down selection menu,
        arrows move through menu.

                            Param
        completion_list: completion values; type completion_list: list.
        """
        
        # Work with a sorted list
        self._completion_list = sorted(completion_list, key=str.lower)
        
        self.configure(values=completion_list)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """
        Autocomplete the Combobox.

                            Param
        delta: 0, 1 or -1: how to cycle through possible hits
        :type delta: int
        """

        if delta:  
            # need to delete selection otherwise we would fix the current
            # position
            self.delete(self.position, 'end')
    
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
    
        # collect hits
        _hits = []
        for element in self._completion_list:
            # Match case insensitively
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
    
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
    
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
    
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, 'end')
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, 'end')

    def handle_keyrelease(self, event):
        """
        Event handler for the keyrelease event on this widget.

        :param event: Tkinter event
        """
        if event.keysym == 'BackSpace':
            self.position = self.index('insert')

            if self.position == self.index('end'):
                self.autocomplete()
                
            return
        
        if event.keysym == 'Left':
            if self.position < self.index('end'):  # delete the selection
                self.delete(self.position, 'end')
        
        if event.keysym == 'Right':
            self.position = self.index('end')  # go to end (no selection)
        
        if event.keysym == 'Return':
            self.handle_return(None)
            return

        if len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

    def handle_return(self, event):
        """
        Function to bind to the Enter/Return key so if Enter is 
        pressed the selection is cleared and text user is confirm.

                        Param
        
        event: Tkinter event or None.
        """
        self.icursor('end')
        self.selection_clear()
        self._comfirm_text(event)

    def config(self, **kwargs):
        """Alias for configure"""
        self.configure(**kwargs)

    def configure(self, **kwargs):
        """Configure widget specific keyword arguments in addition to class:`Combobox` keyword arguments."""

        if "completevalues" in kwargs:
            self.set_completion_list(kwargs.pop("completevalues"))
        return Combobox.configure(self, **kwargs)

    def cget(self, key):
        """Return value for widget specific keyword arguments"""
        if key == "completevalues":
            return self._completion_list
        return Combobox.cget(self, key)

    def keys(self):
        """Return a list of all resource names of this widget."""
        keys = Combobox.keys(self)
        keys.append("completevalues")
        return keys
    
    def __sync(self):
        if self.sync_v.get() == self.get():
            self.sync_v.delete(0, 'end')
            if self.__text:
                self.sync_v.insert(0, self.__text)
            else:
                ch = list(self.values); ch.remove(self.get())
                self.sync_v.insert(0, choice(ch))
                
    @property
    def values(self):
        # Return the values of this combobox.
        return self['values']
    
    @values.setter
    def values(self): ...
    
    def add_values(self, *kw):
        self['values'] += tuple(kw)
    
    def del_values(self, *kw):
        vls = list(self['values'])
        for x in kw: vls.remove(x)
        self['values'] = tuple(vls)

    def __setitem__(self, key, value):
        self.configure(**{key: value})

    def __getitem__(self, item):
        return self.cget(item)
    

class OTBCombobox(Frame):

    # Name: Open Translation Box for Combobox
    # Probide of box for OTACombobox..

    def __init__(self, master, text='From: ', text2='To: ', text_arrow='->',
                 **keyword):
        super().__init__(master, **keyword)
        self.text = text
        self.text2 = text2
        self.separator = Frame(self, width=12)
        self.label_from = Label(self, text=text)

        idioms = self.master.commands('see idioms')
        self.combobox_from = OTACombobox(self, idioms)
        self.label_arrow = Label(self, text=text_arrow)
        self.label_to = Label(self, text=text2)
        self.combobox_to = OTACombobox(self, idioms)

    def set_combo(self):
        self.combobox_from.set(self.master.commands('see lan source'))
        self.combobox_to.set(self.master.commands('see lan target'))

    def start(self):
        self.separator.pack(side='left')
        self.label_from.pack(side='left')
        self.combobox_from.pack(side='left')

        self.label_arrow.pack(side='left')
       
        self.label_to.pack(side='left')
        self.combobox_to.pack(side='left')
        self.pack(side='top', fill='x', expand=False)
        self.set_combo()
        self.combobox_from.sync_v = self.combobox_to
        self.combobox_to.sync_v = self.combobox_from
# import importlib; importlib.reload(modulename)