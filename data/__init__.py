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

#1031bytes 1,00kb

class InterfaceError(BaseException):
    def __init__(self, text):
        self.text = text
        super().__init__(text)
    
    def __str__(self):
        return f"Unknown interfaze: {self.text}"


def interface(name, file, output, notice):
    Interface = ''
    
    if name == 'console':
      from .otconsole import Interface

    elif name == 'graphic': 
      from .otgraphic import Interface
    
    elif name == 'commands': 
      from .otcommands import Interface
    
    if not isinstance(Interface, str):
        return Interface(file, output, notice)
    else:
        raise InterfaceError(name)