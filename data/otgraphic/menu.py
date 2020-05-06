#!/usr/bin/env python
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
Script Name: menu.py
The Widget of menu for OT.
"""

from tkinter import Menu as TkMenu

class Menu(TkMenu):
    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw, tearoff=0)
        
    def load(self, master, empties):
        #  Create cascade or command
        for x in empties:
            
            if isinstance(empties[x], dict):
                obj = Menu(master)
                self.load(obj, empties[x])
                self.make_cascades(master, x, obj)
            else:
                self.make_comandes(master, x, empties[x])
    
    def make_cascades(self, master, label, menu):
        master.add_cascade(label=label, menu=menu)
    
    def make_comandes(self, master, label, commamd):
        if label[-10:] == ' separator':
            master.add_command(label=label[:-10], command=commamd)
            master.add_separator()
        else:
            master.add_command(label=label, command=commamd)

class OTMenu(Menu):
    def __init__(self, master, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.topbar = {'System': {'Config separator': self.master.top_conf,
                                  'Exit': self.master.destroy
                                    },
                       'Translate': {
                                'Save result': self.master.save_result,
                                'Translate file': self.master.tranlate_file,
                                'Translate file and save result': self.master.save_tranlate_file
                                },
                       'View History': lambda: print("h"),
                       'Help': {
                           'Check for Updates': lambda: print("updates"),
                           'About OT': self.master.top_about
                       }
                      }
        
    def start(self):
        self.master['menu'] = self
        self.load()

    def load(self, master=None, empties=None):
        super().load(master or self, empties or self.topbar)