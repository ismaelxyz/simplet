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
Script Name: boxcenter.py
"""

from tkinter.ttk import Frame, PanedWindow
from .scrollbar import OTScrollbar
from .text import OTText


class BoxCenter(Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.__text = ''
    
    def start(self):
        # Init the main process of this class.
        
        self.paned = PanedWindow(self, orient='horizontal')
        fr, self.text_translate = self.make_box_translate(self.paned)
        fr2, self.text_translation = self.make_box_translate(self.paned)
        self.text_translation['state'] = 'disable'
        self.paned.add(fr)
        self.paned.add(fr2)
        self.paned.pack(fill='both', expand='yes')
        self.pack(fill='both', side='top', expand='yes')
    
    def make_box_translate(self, master):
        # Create a frame and over it create a text whit horizontal
        # and vertical OTScrollbar.

        ## Param
        #   master: Master of the frame.

        # Return: frame and text.

        text_frame = Frame(master)
        text = OTText(text_frame, wrap='none')

        for x in [('left', 'y', 'vertical'), ('bottom', 'x', 'horizontal')]:
            scroll = OTScrollbar(text_frame, orient=x[2])
            scroll['command'] = eval(f"text.{x[1]}view")
            scroll.pack(side=x[0], fill=x[1])
            text[f"{x[1]}scrollcommand"] = scroll.set
        text.pack(fill='both', expand='yes')
        text.window_create('1.0')

        return text_frame, text
    
    @property
    def __txt_get(self):
        return self.text_translate.get('1.0', 'end')