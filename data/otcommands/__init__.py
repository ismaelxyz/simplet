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


# Script Name: commands/__init__.py
# Interface of commands for OT.

from data.kernel import BaseInterface
from .commands import OTCommands
from sys import stderr


class Interface(OTCommands, BaseInterface):

    def __init__(self, *kw):
        # BaseInterface __init__
        self.__output = False
        if len(kw) == 2: 
            self.__output = kw[1]
        super().__init__('commands', *kw)
    
    def process(self):
        self.print_notice()
        print()
        if self._file_and_output in (3, 1):
            stderr.write('Error: Not give input file.\n')
        
        else:
            self.show_file()