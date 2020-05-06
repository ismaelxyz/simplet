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
Script Name: console.py
Support for interface console for OT.
"""

class OTConsole(object):
    
    def __init__(self):
        self.__close = False
    
    def commands(self, command):
        if command == 'exit':
            return 'Bye.'

    def translate(self, text):
        return f"Translation:\n\n {text}\n"
    
    def process(self):
        from time import sleep

        while self.__close == False:
            text = input(">: ")
    
            if '.\\' == text[0:2]:
                print('\n', self.commands(text[2:]))

            else:
                print('\n', self.translate(text))
                sleep(0.5)
                
    def destroy(self):
        self.__close = True