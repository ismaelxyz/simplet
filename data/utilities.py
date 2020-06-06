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
Script Name: utilities.py
"""

from os import makedirs
from os.path import isdir, dirname, isfile, abspath
from pathlib import Path
from yaml import Loader, Dumper
from io import StringIO
from os.path import join
# from os import linesep
# statinfo = os.stat('somefile.txt')
# os.add_dll_directory(path)

def camel_space_case(string):
    n_string = ''
    s = '_'  # Virtual separator.
    if s not in string and ' ' in string: s = ' '
    for s in string.split(s):
        if 'ot' != s:
            n_string += s.capitalize() + ' '
        else:
            n_string += 'OT '

    return n_string.rstrip()

# Functions for dirs.
def force_path(*path):
    for x in path:
        if not isdir(x):
            makedirs(x)

def find_with_glob(base, how, clear=False, spaces=' '):

    if base == 'data':
        base = dirname(abspath(__file__))
    
    if base.startswith('data+'):
        base = join(dirname(abspath(__file__)), base[5:])
        
    rang = Path(base)
        # /bindtext.tcl # '*/bindtext.tcl'
    result = rang.glob(how)
    
    if clear:
        return [str(x.as_posix()).replace(' ', spaces) for x in result]
    
    return [str(x).replace(' ', spaces) for x in result]


# Functions for files.
def write_file(file, data, mode='w'):
    with open(file, mode=mode, encoding='utf-8', newline='\n') as paper:
        paper.write(data)
        paper.close()

def append_file(file, data, mode='a'):
    write_file(file, data, mode)

def read_file(file, mode='r'):
    with open(file, mode=mode, encoding='utf-8', newline='\n') as paper:
        data = paper.read()
        paper.close()
    return data

def read_file_error(file):
    try:
        return read_file(file)

    except FileNotFoundError:
        return ['Error: File not exists.']
    
    except PermissionError:
        return ['Error: Permission insufficient.']

# Functions for YAML files.
def yaml_load(file, mode='r'):
    
    with open(file, mode=mode, encoding='utf-8', newline='\n') as paper:
        load = Loader(paper)
        data = load.get_data()
        paper.close()
    return data

def yaml_dump(file, data, mode='w'):
    # mode: w/wb
    with open(file, mode=mode, encoding='utf-8', newline='\n') as paper:

        dump = Dumper(paper)
        dump.open()
        dump.represent(data)
        dump.close()

        paper.close()

def yaml_load_except(file, _type={}, mode='w'):
    try:
        return yaml_load(file) or _type
    except FileNotFoundError:
        return _type

def yaml_append(file, data, seccion=False, re=False, _type={}, recursive=False):
    old_data = yaml_load_except(file, _type)

    if seccion:
        if seccion in old_data:
            old_data[seccion].update(data)
        else:
            old_data.update({seccion: data})
    else:

        if isinstance(_type, dict):
            old_data.update(data)
        
        if isinstance(_type, list):
            for x in data:
                if recursive:
                    old_data.append(x)

                else:
                    if x not in old_data:
                        old_data.append(x)
        
    yaml_dump(file, old_data)
    if re:
        return old_data

# Functions for YAML.
def yaml_read(string, mode='r'):
   
    return Loader(string).get_data()
    