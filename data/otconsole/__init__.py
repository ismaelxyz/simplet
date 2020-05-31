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
Script Name: otconsole/__init__.py
Interface console for OT.
"""

from .console import OTConsole
from data.kernel import BaseInterface
from .otcolorama import init, Fore, Back
from sys import stderr

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
        #### Deprecate
        text = BaseInterface.translate(self, text)

        if self.error_ocurred:
            return text  # Text of Error.

        return super().translate(text)
    
    def process(self):
        self.print_notice()
        super().process()
    
    def commands(self, args: list):

        if args[0] == 'consult':
            if args[1] == 'user':
                self.show_message(self.consult_user(args[2]))
        
        elif args[0] == 'file':
             self.translate_file(input('File to translate: '), 
                                 input('\nSave in file?: '))
        
        elif args[0] == 'change':
            
            if self.change(*args[1:]):
                self.show_message('Done change.')
            else:
                self.show_message('Fail change.')
                
        elif args[0] == 'insert':
            if args[1] == 'idioms':
                self.insert_idioms(*args[2:])
        
        elif args[0] == 'see':
            result = str(self.see_config(*args[1:]) or '')
            self.show_message(args[-1] + '\n\t' + result) if result else ...
        
        elif args[0] == 'del':
            self.delete_these(*args[1:])
        
        if args[0] == 'save':
           self.save_translation(input('Text to translate: '), 
                                 input('\nSave in file?: '))

        if args[0] == 'search':
            if args[1].isdigit():
                args[1] = int(args[1])
            self.search_in_record(*args[1:])
        
        elif args[0] == 'file ':
            self.show_message(self.translate_file(input('File to translate?: '), 
                                                  input('Save in file?: ')))
        
        elif args[0] == 'exit':
            super().commands()
            self.destroy()
        """
        XXX In the future implement
        import sys
        sys.stdin.read()
        ^Z for exit
        """