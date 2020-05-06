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
Script Name: kernel.py
The kernel of OT, manager of the work hard.
"""

from .settings import *
from os import linesep
from .constans import NOTICE


class BaseInterface(object):
    """
    El padre de todas las interfaces en OT.
    Es el gerente de los errores, la información (en general)
    """

    def __init__(self, name, file=None, output=None, logo=True):
        """
        Initialize interface whit her special extensions and
        the translate.

                        Params
        name: name of the interfaze in activity.
        file: File to translate.
        output: File of output translation.  
        logo: Print notice program.
        """

        from .extensions import Extensions
        from .translator import Translator
        from .utilities import write_file

        os_info = init_settings()  # Initialize settings.

        self.__write_file = write_file

        # Protected attributes!
        self.__file, self.__output, self.__logo = file, output, logo

        # Initialize and sync data app whit interactive data.
        self._t = Translator(
            *get_setting('source', 'target', 'headers', 'url'))
        
        self.ext = Extensions(os_info('Home Ext'))
        self.__consult_user = os_info
        # Preload Extensions (load metadata).
        self.ext.load(name)
        self.info_ext = self.ext.info_extensions

        # List of settings abalibles for change.
        self._list_settings = ['source', 'target', 'headers', 'url', 'language']
        self.__error_ocurred = False
    
    def internal_record(action):
        if action == 'read':
            pass

    @property
    def error_ocurred(self):
        # No doc, in develop.

        if self.__error_ocurred:
            self.__error_ocurred = False
            return True
        return False

    def print_notice(self):
        """Print an introduction a OT."""
        if self.__logo:
            print(NOTICE)

    def commands(self, command, what=None, **keyward):
        """Run commands of OT."""

        argv = command.split(' ')[1:]
        command = command.split(' ')[0]

        out = False
        if 'file' in keyward:
            file = keyward['file']
        if 'out' in keyward:
            out = keyward['out']

        if command == 'exit':
            self.destroy()
            return ''
        
        elif command == 'consult':
            if argv[0] == 'user':
                return self.__consult_user(what)

        elif command == 'file':
            return self._t.file_translate(file, out)

        elif command == 'change':
            if argv[0] == 'lan':
                if argv[1] == 'source':
                    self._t.source = argv[2]
                if argv[1] == 'target':
                    self._t.target = argv[2]
            elif argv[0] == 'headers':
                self._t.headers = argv[1]
            elif argv[0] == 'url':
                self._t.url = argv[1]
            
            if argv[0] in self._list_settings or\
               argv[1] in self._list_settings:
                set_setting({argv[-2]: argv[-1]})
                print(get_setting('theme'))

        elif command == 'insert':
            if argv[0] == 'idiom':
                self._t.source = argv[1]
                add_idioms(argv[1])

        elif command == 'see':

            if argv[0] == 'lan':
                if argv[1] == 'source':
                    return self._t.source
                elif argv[1] == 'target':
                    return self._t.target
            elif argv[0] == 'idioms':
                return get_idioms()
            elif argv[0] == 'headers':
                return self._t.headers
            elif argv[0] == 'url':
                return self._t.url
            elif argv[0] == 'all':
                return self._t.see_all()
            # size in len not in bytes; NOTE: Create space for bytes
            elif argv[0] == 'size':
                return self._t.size()
            elif argv[0] in self._list_settings:
                return get_setting(argv[0])

        elif command == 'del':
            return f"{self._t.del_histori(int(argv[0]))}"

        elif command == 'save':
            for x in argv:
                argv[0] += ' ' + x
            return self._t.save_translation(argv[0].rstrip(), out)

        elif command == 'search':
            if command.isdigit():
                command = int(command)
            return self._t.search(*argv)

        else:
            return f"Error: Unknown command: {command}."

    def _view_translate(self, data):
        raise NotImplementedError('This methods is for subclass.')
    
    def create_error(self, info):
        # If info is type list an error as ocurred in this case capture these
        # error.

        if isinstance(info, list):
            self.__error_ocurred = True
            info = info[0]
        return info

    def translate(self, text):
        text = self._t.translate(text)
        
        return self.create_error(text)

    @property
    def _file_and_output(self):
        """Return an virtual state."""

        if self.__file and self.__output:
            return 0

        elif not self.__file and self.__output:
            return 1

        elif self.__file and not self.__output:
            return 2

        elif not self.__file and not self.__output:
            return 3

    def show_file(self):
        """
        Traducir un archivo y si es solicitado salvar la
        traducción.
        """
        if self.__file:
            data = self.commands('file', file=self.__file, out=self.__output)
            if isinstance(data, list):
                data = data[1][0]
            self._view_translate(data)

    def output_file(self):
        """
        Save translation of interaction in the interface active.
        """
        exit("In output_file")

        self.__write_file(self.__output, text)

    def process(self):
        """
        The main process of all interfaces.

        The code of your subclass here!
        El codigo de aqui es el interactivo al ser interunpido se guardan los
        datos si o si!
        """
        raise NotImplementedError('This methods is for subclass.')

    def not_interrupt(self):
        """Control of Errors."""
        try:
            self.process()
        except KeyboardInterrupt:
            print('Interrupt for Key')
            self.commands('exit')

    def mainloop(self):
        """Main loop for all interfaces."""
        self.not_interrupt()

    def destroy(self):
        """This methods is for subclass."""
        pass