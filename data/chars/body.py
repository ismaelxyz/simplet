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

from os.path import isfile
import re
def separate_lines(text):
    pass

def load_file(_file):
    return open(_file, 'r').readlines()

def start(_file):
    data = []
    if isfile(_file) and _file[:-3] == '.cr':
        file_cr = load_file(_file)
    else:
        return
    
    system = ''
    tr_cr = ''
    count = 0
    pretranslate = ''

    while True:
          # translate word
        if '//' in file_cr[0]:
            pretranslate = file_cr[:file_cr.index('//')]