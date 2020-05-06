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


class TopAbout(OTToplevel):

    def __init__(self, master, title='Open Translation: About'):
        super().__init__(master, title)
        self['bg'] = "red"

        self.fr = Frame(self)
        self.fr.pack(fill='both', expand='yes')
        
        self.lb = Label(self.fr, name="logo") # Label for logo
        self.lb.pack(pady=4)

        path_logo = find_with_glob(join('data+otgraphic', 'images'),
                                        '*logo48.png', True)[0]
        self.tk.eval(f"display_logo {path_logo}")
        
        self.note = Notebook(self.fr)
        self.note.pack(fill='both', expand='yes')

        self.tab_app = Frame(self.note)
        self.note.add(self.tab_app, text="Application")
        self.label_app()

        self.tab_author = Frame(self.note)
        self.note.add(self.tab_author, text="Author")
        self.label_author()

        self.tab_license = Frame(self.note)
        self.note.add(self.tab_license, text="License")
        self.widget_license()

    
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

"""
ven = Tk()
asd = TopHelp(ven)
ven.mainloop()


Version: 1.44.2 (user setup)
Commit: ff915844119ce9485abfe8aa9076ec76b5300ddd
Date: 2020-04-16T16:33:57.013Z
Electron: 7.1.11
Chrome: 78.0.3904.130
Node.js: 12.8.1
V8: 7.8.279.23-electron.0
OS: Windows_NT ia32 6.1.7601
"""