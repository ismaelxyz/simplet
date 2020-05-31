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

"""
Script Name: topconf.py
Widget of settings of OTGraphic.
"""

from tkinter.ttk import Frame, Button, Style, LabelFrame, Label
# from data.utilities import yaml_load_except, force_path, yaml_dump
from ..toplevel import OTToplevel
from ..combobox import OTACombobox
from .boxcanvas import BoxCanvas


class TopConf(OTToplevel):

    def __init__(self, master: str, title: str='Configuration'):
        super().__init__(master, title)
        
        self.screens.update(Language=self.language, Record=self.record,
                        Internal=self.internal, Intelligence=self.intelligence,
                        Extensions=self.extensions)
        
        self._config = {'language': self.master.see_config('language'),
                         'languages': self.master.ext.search('language',
                                                            what='name'),
                         'screen': 'language',
                         'extensions': {'enabled': {}, 'disabled': {}}
        }
        
        self._sync_conf('conf')
        
        self.__vertical_butoms()
        getattr(self, self._config['screen'])()
        
        # "#9e9a91"
        # #eaeaea #afaf9f

    def set_configuration(self, key, value, ke2=None):
        self._config[key] = value
        if key in self.master._list_settings:
            self.master.change(key, value, ke2)

    def __vertical_butoms(self):
        left = Frame(self, name='left')
        for x in self.screens:
            x = Button(left, text=x, command=self.screens[x])
            self.opack(x, side='top')
        left.pack(side='left', fill='y')
    
    # Frames
    def basic_box(self, text, values, key):
        fr = Frame(self, style='fr2.TFrame')
            
        fr.pack(fill='both', expand='yes')
        fr.rowconfigure(4, weight=2, pad=5, minsize=10)
        fr.columnconfigure(4, weight=2, minsize=0)

        lfe = Frame(fr)
        lfe.grid(column=4, pady=5, row=2)

        ll = Label(lfe, text=text, style='la2.TLabel')
        ll.pack(padx=5, side='left')

        # TopCombobox
        otacx = OTACombobox(lfe, key, self.set_configuration,
                            self._config[values])
                            
        otacx.set(self._config[key])
        otacx.pack(pady=5, padx=10, side='left')

    def language(self):
        
        if self._clear_screen('language'):
            self.basic_box('Language of the Interface', 'languages', 'language')
            
    def record(self):
        if self._clear_screen('record'):
            print('record')
    
    def intelligence(self):
        if self._clear_screen('intelligence'):
            print("intel")
    
    def internal(self):
        if self._clear_screen('internal'):
            print("internal")
    
    def extensions(self):
        if self._clear_screen('extensions'):
            list_ext = self.master.ext.search('all', state=True)
            b_can = BoxCanvas(self)
            b_can.pack(fill='both', expand='yes')
            b_can.tk.eval(f"canvas_style {b_can.canvas}")
    
    def destroy(self):
        """Save config and delete widget."""
        del self._config['languages'], self._config['language']
        super().destroy('conf')