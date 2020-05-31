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
Script Name: help.py
Widget of help for OTGraphic.
"""

from tkinter import Toplevel, Tk, Text
from tkinter.ttk import Frame, Label, Button
from data.constans import AUTHOR, AUTHOR_EMAIL, VERSION, COMMIT, BRANCH, \
    LICENSE, REPOSITORY, COPYRIGHT
from .toplevel import OTToplevel
from tkinter.ttk import Notebook
from data.utilities import find_with_glob, read_file
from os.path import join


# TopFrame(): 

class TopAbout(OTToplevel):

    def __init__(self, master, title='About'):
        super().__init__(master, title)

        self['bg'] = "red"

        self.index = {
            'application': 0,
            'author': 1,
            'license': 2
        }
        self._config = {'screen': 'application'}
        
        self._sync_conf('about')

        self.fr = Frame(self)
        self.fr.pack(fill='both', expand='yes')
        
        self.lb = Label(self.fr) # Label for logo
        self.lb.pack(pady=7)

        path_logo = find_with_glob(join('data+otgraphic', 'images'),
                                        '*logo117.png', True)[0]
        self.tk.eval(f"display_logo {path_logo} {self.lb}")
        
        self.note = Notebook(self.fr)
        self.note.pack(fill='both', expand='yes')

        self.tab_app = Frame(self.note, name='application')
        self.note.add(self.tab_app, text='Application')
        self.label_app()

        self.tab_author = Frame(self.note, name='author')
        self.note.add(self.tab_author, text='Author')
        self.label_author()

        self.tab_license = Frame(self.note, name='license')
        self.note.add(self.tab_license, text='License')
        self.widget_license()

        self.note.enable_traversal()
        self.note.select(self.index[self._config['screen']])
        self.note.bind('<ButtonPress>', lambda x: self._clear_screen())
    
    def set_configuration(self, *kw):
        self._config[kw[0]] = kw[1]

    def __to_call(self):
        """Call to  _clear_screen (SuperClass); NOTE: Error in lambda."""
        super()._clear_screen(self.note.select().split('.')[-1], False)

    def _clear_screen(self):
        self.after(120, self.__to_call)
    
    def label_app(self):
        self.lba = Label(self.tab_app, text=self.text_app())
        self.lba.pack(pady=4)
    
    def text_app(self) -> str:
        text = ""
        
        for x in (f"Version: {VERSION}", f"Commit: {COMMIT}", 
                  f"Branch: {BRANCH}", f"License: {LICENSE}",
                  f"Repository: {REPOSITORY}", f"Copyright: {COPYRIGHT}"):
            text += x + "\n"
        return text
    
    def label_author(self):
        self.lbu = Label(self.tab_author, text=self.text_author())
        self.lbu.pack(pady=4)
    
    def text_author(self) -> str:
        text = ""
        
        for x in (f"Author: {AUTHOR}", f"Author Email: {AUTHOR_EMAIL}"):
            text += x + "\n"
        return text
    
    def widget_license(self):
        from .text import OTText
        from .scrollbar import OTScrollbar
        
        text = OTText(self.tab_license, wrap='none')

        for x in [('right', 'y', 'vertical'), ('bottom', 'x', 'horizontal')]:
            scroll = OTScrollbar(self.tab_license, orient=x[2])
            scroll['command'] = eval(f"text.{x[1]}view")
            scroll.pack(side=x[0], fill=x[1])
            text[f"{x[1]}scrollcommand"] = scroll.set
        text.insert('1.0', read_file(find_with_glob('data+legal',
                                                    '*COPYRIGHT.txt')[0]))
        text['font'] = ('Liberation Serif', 10, 'normal')
        text['state'] = 'disable'
        # FangSong
        self.tk.eval(f"text_stylize {text}")
        text.pack(fill='both', expand='yes')
        text.window_create('1.0')
    
    def destroy(self):
        super().destroy('about')