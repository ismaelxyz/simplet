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
Script Name: console.py
Support for interface console for OT.
"""

from sys import stderr

class OTConsole(object):
    
    def __init__(self):
    
        self.__close = False
    
    def commands(self, command: None=None):
        # This method is for subclass.
        self.show_message('Bye.')
        
    def show_message(self, text: str):
        skip = ''
        if text in ('Interrupt for Key', 'Bye.'):
            skip = "\n"

        elif text[-2:] != '\n\n':
            # XXX: Problen whit ending line in the end of program.
            skip = '\n' if '\n' == text[-1] else '\n\n'
        stderr.write(text + skip) 

    def translate(self, text):
        return f"Translation:\n\t{text}"
    
    def process(self):
        from time import sleep

        print()
        while self.__close == False:
            text = input(">: ").strip()
            # print(end='\n')
            
            if '.\\' == text[0:2]:
                self.commands(text[2:].split(' '))

            else:
                text = self.translate(text)
                self.show_message(text) if text else ''
                sleep(0.5)

    def destroy(self):
        self.__close = True