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


# Script Name: otgraphic/__init__.py

from tkinter.ttk import Style
from .windows import OTWindows
from data.kernel import BaseInterface
from data.utilities import write_file, find_with_glob
from os.path import realpath
from os.path import join
from tkinter import PhotoImage


class Interface(OTWindows, BaseInterface):

    def __init__(self, *kw):
 
        super().__init__()
        BaseInterface.__init__(self, 'graphic', *kw)
        
        # NOTE: self.command is different of self.commands
        # self.command is internal of Tkinter
        # self.commands is internal of OT

        self._list_settings.append('theme')
        self._list_settings.append('arrow')
        # List of themes (Only for windows?).
        #('winnative', 'clam', 'alt', 'default',
        # 'classic', 'vista', 'xpnative')

    def changet_theme(self, theme: str=''):

        # changet actual theme

        # Para que esta aplicación pueda cargar su tema
        # debe estar en la carpeta extensions dentro
        # de una carpeta con el nombre del tema y el archivo
        # principal tambien debe llevar el nombre del tema.

        # Nota: el thema debe estar codificado en tcl (tk/tcl)
        if theme == '':
            theme = self.commands('see theme')

        if theme in self.commands('see themes'):

            theme = self.ext.search('theme', theme)
            if theme['main file'].endswith('.tcl'):
                path = realpath(theme['path'])
                path = path.replace('\\', '/')

                self.tk.eval(f"source {path}/{theme['main file']}")
                self.tk.eval(f"ttk::style theme use {theme['call to']}")

        elif theme in self.tk.eval('ttk::style theme names').split(' '):
            self.tk.eval(f"ttk::style theme use {theme}")
    
    def create_default_commands(self):
        # This is for Tk 
        self.tk.createcommand('package_dir', self.ext.pack_name)
        self.tk.createcommand('do_translation', self.__translate)
        self.tk.createcommand('find_with_glob', find_with_glob)
        super().create_default_commands()
            
    def process(self):
        super().start()
        self.geometry('600x450+450+150')
        self.translate['width'] = 35
        self.changet_theme()
        #self.top_conf()
        self.create_default_commands()
        
        
        """
        from os.path import isdir, dirname, isfile, abspath,normcase, normpath
        from pathlib import Path, PurePath, WindowsPath, PurePosixPath, PosixPath
        
        fa = Path(search_dir(f"{search_dir('data')}/otgraphic"))
        # /bindtext.tcl
        be = fa.glob('*/bindtext.tcl')
        # .as_posix() Return a string representation of the path with forward slashes (/):
        # stem: name obj
        # name: name of path example 'bindtext.tcl'
        # suffix: name of extension  example .tcl
        """
        bind_text = find_with_glob('data', '*/bindtext.tcl', True)[0]
        self.tk.eval(f"source {bind_text}")
        # self.commands('change theme Door')
        
        super().mainloop()
    
    def __show_error(self, text: str):
        return text[0][7:].capitalize()

    def __translate(self, text: str):
        text = self._t.translate(text)

        if isinstance(text, list):  # Ocurred a Error.
            self.statusbar.show_message(self.__show_error(text))
            text = ''

        return text

    def commands(self, command: str, *args, **kwards):
        cm = command.split(' ')
        if cm[0] == 'change':
            if cm[1] == 'theme':
                self.changet_theme(cm[2])

            elif command == 'arrow':
                pass
        
        elif cm[0] == 'see':
            if cm[1] == 'themes':
                return self.ext.search('theme', what='name')
                
        return super().commands(command, *args, **kwards)  # officialese changes

    def save_result(self):
        out = super().save_result()
        if out:
            text = self.translation.get('1.0', 'end')
            write_file(out, text)
            self.statusbar.show_message(f"Save translation in file: {out}.")
        else:
            # OPTIMIZE: /home/user/out.tc 
            self.statusbar.show_message(f"Abort save of translation in file.")

    def tranlate_file(self):
        file = super().tranlate_file()

        if file == '':
            self.statusbar.show_message(f"Abort translation of file.")
            return
        
        text = self.commands('file', file=file)

        if isinstance(text, str):
            self.translation.insert_disable('1.0', text)
            self.statusbar.show_message(f"Translate file: {text}.")
        else:
            self.statusbar.show_message(self.__show_error(text))

    def save_tranlate_file(self):
        
        """
        _file='translate.cr'
        f_result='translation.tc'
        """
        file, out = super().save_tranlate_file()

        if file == '' or out == '':
            self.statusbar.show_message(f"Abort translation and save of file.")
            return

        data = self.commands('file', file=file, out=out)
        if isinstance(data, str):
            self.translation.insert_disable('1.0', data)
            self.statusbar.show_message(f"Translate file: {file}.")
        else:
            self.statusbar.show_message(self.__show_error(data))

    def mainloop(self):
        # This not is mainloop for widget
        # This is mainloop for Interface
        BaseInterface.mainloop(self)


