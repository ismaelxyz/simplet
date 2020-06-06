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
Script Name: otgraphic/__init__.py
"""

from .windows import OTWindows
from data.kernel import BaseInterface
from data.utilities import write_file, find_with_glob
from os.path import join
from threading import Thread
        
    
class  Interface(OTWindows, BaseInterface):

    def __init__(self, *kw):

        super().__init__()
        from data.checkconnection import check_connection
        self.tk.createcommand('check_connection', check_connection)
        BaseInterface.__init__(self, 'graphic', *kw)

        self._list_settings.append('theme')
        self._list_settings.append('arrow')
        
    def show_message(self, text: str, time: int=2500):
        if text.startswith('Error: '):
            text = text[7:].capitalize()
        self.tk.call("show_message", text, time)

    def changet_theme(self, theme: str=''):

        # changet actual theme

        # Para que esta aplicación pueda cargar su tema
        # debe estar en la carpeta extensions dentro
        # de una carpeta con el nombre del tema y el archivo
        # principal tambien debe llevar el nombre del tema.

        # Nota: el thema debe estar codificado en tcl (tk/tcl)
        if theme == '':
            theme = self.see_config('theme')

        if theme in self.ext.search('theme', what='name'):

            theme = self.ext.search('theme', theme)
            if theme['main file'].endswith('.tcl'):
                path = __import__('os').path.realpath(theme['path'])
                path = path.replace('\\', '/')

                self.tk.eval(f"source {path}/{theme['main file']}")
                self.tk.eval(f"ttk::style theme use {theme['call to']}")

        elif theme in self.tk.eval('ttk::style theme names').split(' '):
            self.tk.eval(f"ttk::style theme use {theme}")
    
    def __create_default_commands(self):
        # This is for Tk

        self.tk.createcommand('package_dir', self.ext.pack_name)
        self.tk.createcommand('do_translation', self.__translate)
        super().create_default_commands()

    def process(self):
        super().start()
        self.geometry('610x490+450+150')
        self.translate['width'] = 35
        self.changet_theme()
        #self.top_conf()
        self.__create_default_commands()
        
        bind_text = find_with_glob('data', '*/bindtext.tcl', True)[0]
        self.tk.eval(f"source {bind_text}")
        # self.charge('theme', 'Door')
        super().mainloop()

    def __translate(self, text: str):
        
        def call_translate():
            nonlocal text
            text = self._t.translate(text)
        
        one = Thread(name='one', target=call_translate)
        one.start()
        one.join()
        
        return self._capture_error(text)

    def save_result(self):
        out = super().save_result()
        if out:
            text = self.translation.get('1.0', 'end')
            write_file(out, text)
            self.show_message(f"Save translation in file: {out}.")
        else:
            # OPTIMIZE: /home/user/out.tc 
            self.show_message(f"Abort save of translation in file.")

    def tranlate_file(self):
        file = super().tranlate_file()

        if file == '':
            self.show_message(f"Abort translation of file.")
            return None
        
        text = self._capture_error(self.commands('file', file=file))

        if text != '':
            self.translation.insert_disable('1.0', text)
            self.show_message(f"Translate file: {text}.")

    def save_tranlate_file(self):
        
        """
        _file='translate.cr'
        f_result='translation.tc'
        """
        
        file, out = super().save_tranlate_file()

        if file == '' or out == '':
            self.show_message(f"Abort translation and save of file.")
            return

        data = self._capture_error(self.commands('file', file=file, out=out))
        
        if data != '':
            self.translation.insert_disable('1.0', data)
            self.show_message(f"Translate file: {file}.")

    def mainloop(self):
        # This not is mainloop for widget
        # This is mainloop for Interface
        BaseInterface.mainloop(self)