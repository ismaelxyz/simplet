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
from data.utilities import yaml_append 


class BaseInterface(object):
    """
    The father of all interfaces in OT.
    By the manager of errors and information (in general).
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
    
    def internal_record(self, action):
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

    def translate_file(self, _file: str, out: str=''):
        return self._capture_error(self._t.file_translate(_file, out))
    
    def consult_user(self, what):
        return self.__consult_user(what)
    
    def change(self, what, n_value, what2=None):
        what = what2 or what
    
        if hasattr(self._t, what):
            setattr(self._t, what, n_value)
            
        if what in self._list_settings:
            set_setting({what: n_value})
            return True
    
    def insert_idioms(self, *kw):
        add_idioms(*kw)

    def see_config(self, what, what2=None):
        
        if what == 'lan':

            if what2 == 'source':
                return self._t.source

            elif what2 == 'target':
                return self._t.target
           
        elif what == 'idioms':
            return get_idioms()
           
        elif what == 'headers':
            return self._t.headers
           
        elif what == 'url':
            return self._t.url
           
        elif what == 'all':
            return self._t.see_all()
           
        elif what == 'size':
            # size in len not in bytes; NOTE: Create space for bytes
            return self._t.size()
        
        elif what in self._list_settings:
            return get_setting(what)
    
    def delete_these(self, these, *value):
        # ;)
        if these == 'record':
            return f"{self._t.del_histori(value[0])}"
            
        if these == 'idioms':
            del_idioms(*value)
            return True
    
    def save_translation(self, text, file_out):
        return self._capture_error(self._t.save_translation(text, file_out))
    
    def search_in_record(self, *argv):
        self._capture_error(self._t.search(*argv))

    def _view_translate(self, data):
        raise NotImplementedError('This methods is for subclass.')

    def show_message(self, text: str):
        """Show message for the user."""
        raise NotImplementedError("This method is for subclass.")
    
    def _capture_error(self, info):
        # If info is type list an error as ocurred in this case capture these
        # error and send message.

        if isinstance(info, list):
            self.__error_ocurred = True
            self.show_message(info[0])
            info = ''
        return info

    def translate(self, text):
        return self._capture_error(self._t.translate(text))

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
            self._view_translate(self.translate_file(self.__file, self.__output))

    def output_file(self):
        """
        Save translation of interaction in the interface active.
        """
        exit("In output_file")

        # self.__write_file(self.__output, text)

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
            self.show_message('Interrupt for Key')
            self.destroy()

    def mainloop(self):
        """Main loop for all interfaces."""
        self.not_interrupt()

    def destroy(self, _file='history.yml'):
        """This methods is for subclass."""
        yaml_append(_file, self._t.search('all'))