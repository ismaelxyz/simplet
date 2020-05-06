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


# Script Name: otconsole/__init__.py
# Interface console for OT.

from .console import OTConsole
from data.kernel import BaseInterface
from .otcolorama import init, Fore, Back
"""
# from otcolorama.winterm import WinTerm
init()
print("sopa")
print(Fore.CYAN + "Hola", Back.CYAN + Fore.RED  + "que")
print("estoy")
exit()
"""
class Interface(OTConsole, BaseInterface):

    def __init__(self, *kw):
        super().__init__()
        BaseInterface.__init__(self, 'console', *kw)
    
    def translate(self, text):
        text = BaseInterface.translate(self, text)

        if self.error_ocurred:
            return text + "\n"  # Text of Error.

        return super().translate(text)
    
    def process(self):
        self.print_notice()
        super().process()
    
    def commands(self, command):
        if command[:5] == 'save ':
            return BaseInterface.commands(self, command, 
                   out=input('Save in file?: '))
        
        elif command[:5] == 'file ':
            file=input('File to translate?: ')
            print('')
            out=input('Save in file?: ')
            return BaseInterface.commands(self, command, file=file, out=out)
        
        result = BaseInterface.commands(self, command)
       
        if command == 'exit':
            return super().commands(command)
        """
        XXX In the future implement
        import sys
        sys.stdin.read()
        ^Z for exit
        """
        return result
    
    def destroy(self):
        super().destroy()