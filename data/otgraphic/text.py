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


# Script Name: text.py

# FIXME: DEPRECATE: File delete at the nex version (1.1). 

from tkinter import Text


class OTText(Text):

    def __init__(self, master, wrap):
        super().__init__(master, wrap=wrap)

    def insert(self, index, chars, *args):
        self.delete('1.0', 'end')
        super().insert(index, chars, *args)

    def insert_disable(self, index, chars, *args):
        # insert text in state disable
        
        self['state'] = 'normal'
        self.insert(index, chars, *args)
        self['state'] = 'disable'