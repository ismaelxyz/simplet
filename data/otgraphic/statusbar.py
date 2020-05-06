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


# Script Name: statusbar.py

from tkinter.ttk import Frame
from tkinter import Tk


class StatusBar(Frame):

    from data.checkconnection import check_connection

    def __init__(self, master, name):
        super().__init__(master, name=name)
    
    def destroy_label(self, name):
        self.tk.eval(f"destroy {self}.{name}")
    
    def set_label(self, name, text):
        self.tk.eval(f"{self}.{name} configure -text \"{text}\"")

    def add_label(self, name, text=''):
        if name not in self.children:
            self.tk.eval(f"ttk::label {self}.{name} -text \"{text}\";"
                          f"pack {self}.{name} -side right -padx 2;")
    
    def start(self):
        self.pack(fill='x', expand=False, side='bottom')


class OTSB(StatusBar):
    # Open Translation Status Bar
    def __init__(self, master):
        super().__init__(master, 'opsb')
    
    def show_message(self, text, time=2000):
        ## Params:
        # text: text of the message.
        # time: time of show message in the message label.
        
        self.set_label('message', f"Message: {text}")
        self.after(time, lambda: self.set_label('message', ""))
    
    def confirm_connectivity(self):
        self.set_label('connection', 'Connection status: ' + 
                                  self.check_connection())
    
    def start(self):
        self.add_label('message')
        self.show_message('Welcome.', 4000)
        self.add_label('connection')
        self.confirm_connectivity()
        super().start()