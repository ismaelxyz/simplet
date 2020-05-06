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
Script Name: osinfo.py
Capture necessary info of Os and User for OT.
"""

from data.utilities import camel_space_case, write_file
from base64 import b64decode, b64encode
from tempfile import TemporaryFile


class OsInfo(object):

    def __init__(self):

        self.__element = [
            'architecture',
            'linux_distribution',
            'machine',
            'platform',
            'processor',
            'release',
            'system',
            'version',
            'python_implementation',
            'python_version',
            'python_build',
            'python_compiler',
            'python_branch',
            'python_commit',
            'node'
        ]
        self.__code = 'utf-8'
        self.__info = {}
        self.__capture()
        self.__clear()

    def __dumps(self, text):
        if text is None:
            text = ''
        return bytes(text.encode(self.__code))

    def __loads(self, text):
        return str(text.decode(self.__code))

    def __clear(self, **kwards):
        # Clear lis for convert in pretty (;-)).
        if not kwards:
            kwards = self.__info
        for x in list(kwards):
            self.__info.update({camel_space_case(x):
                                b64encode(self.__dumps(kwards[x]))})
            if x in self.__info:
                del self.__info[x]

    def __capture(self):
        # Capture all info necessary of the user and os.
        import platform as pm
        from getpass import getuser
        from os.path import expanduser

        for key in self.__element:

            if hasattr(pm, key):
                value = str(getattr(pm, key)())
            else:
                value = None
            self.__info.update({f"{key}": value})

        self.__info.update({'user_name': getuser()})

        for x in [['', 'user_profile'], ['/.OpenT', 'home_ot']]:
            self.__info.update({x[1]: expanduser('~') + x[0]})

    def get(self, data):
        # Get info of self.__info.

        if data in self.__info:
            return self.__loads(b64decode(self.__info[data]))
        else:
            return ''

    def add(self, **kwards):
        self.__clear(**kwards)

    def save_data(self):
        # Save data of OS.
        with TemporaryFile(newline='\n') as f:
            for x in list(self.__info):
                f.write(self.__info[x] + '\n')
                # f.close() Your close file

        return f

    def send(self):
        # send the data of OS and App.
        pass


# https://github.com/python/cpython/
# os.linesep
# tempfile.TemporaryFile, TemporaryDirectory
