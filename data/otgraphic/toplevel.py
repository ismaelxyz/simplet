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
Script Name: toplevel.py
Support of toplevel for OTGraphic.
"""

from tkinter import Toplevel
from typing import TypeVar
#from . import create_logo
T = TypeVar('T')

class OTToplevel(Toplevel):

    def __init__(self, master, title: str):
        
        super().__init__(master)
        self.title(title)
        self.grab_set()
        self.transient(master=master)
        self.master.create_logo(self)
        
        # XXX: Formule deficient in full screen.
        size = lambda x: int(x) - int(int(x) * 0.06)
        #  Note: Las pantallas tienen mas x que y (ancho que alto).
        loc_x = lambda x, x2: int(int(x) * 0.03) + int(x2)
        loc_y = lambda x, x2: int(int(x) * 0.045) + int(x2)
        
        a, b = self.master.geometry().split('x')
        b, c, d = b.split('+')
        self.geometry(f"{size(a)}x{size(b)}+{loc_x(a, c)}+{loc_y(b, d)}")

        self.__screen = ''
        self.screens = {}
    
    def opack(self, obj, **kw):
        obj.pack(**kw)

    def set_configuration(self, name: str, value: T):
        raise NotImplementedError("This method is for subclasses.")

    def _clear_screen(self, screen: str):
        """
        Control of screen for interactives toplevels.
        XXX: Please Use with caption.
        """

        if self.__screen != screen:
            self.__screen = screen
            self.set_configuration('screen', screen)

            for x in self.children.copy():
                if x != 'left': self.children[x].destroy()
            return True
        return False