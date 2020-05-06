#! /usr/bin/env python
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
Script Name: extensions/__init__.py
.
"""

from shutil import move
from os.path import isfile, dirname, basename, isdir, join
from os import listdir, remove
from threading import Thread
from sys import path as s_path


class Extensions(object):
    """
    Script Name: extensions/__init__.py
    Load, disability, install, search and uninstall estencions.
    """

    def __init__(self, home_px):
        """
                                    Param

        home_px: Path to home extensions in ".OpenT" (Home OT in home user).
        """
        from data.utilities import yaml_append, yaml_load_except, yaml_dump

        # json_reader: function for read json files.
        self.__dump = yaml_dump
        self.__read = yaml_load_except
        self.__append = yaml_append
        self.__home = home_px  # Home extensions.

        # Path of the extensions.
        self.__pack_dir = home_px + '/package/'
        self.__list_extensions = f"{home_px}/extensions.yml"
        self.__states_extensions = f"{home_px}/states.yml"
        self.__info_extensions = {}
        
        self.__state_extensions = {'enabled': {}, 'disabled': {}}

    @property
    def info_extensions(self):
        """Return a copy info_extensions."""
        return self.__info_extensions.copy()
        
    def state_extensions(self, state=None):
        """Return a copy state_extensions."""
        if state is None:
            return self.__state_extensions.copy()
        return self.__state_extensions.copy()[state]
    
    def __change_state(self, ext, source, target):
        # FIXME: Message of Error.
        
        if ext in self.__state_extensions[source]:
            value = self.__state_extensions[source][ext]
            del self.__state_extensions[source][ext]
            self.__state_extensions[target].update({ext: value})
            self.__dump(self.__states_extensions, self.state_extensions())
    
    def enabled(self, ext):
        # ext: String name of extension.
        self.__change_state(ext, 'disabled', 'enabled')
         
    
    def disabled(self, ext):
        # ext: String name of extension.
        self.__change_state(ext, 'enabled', 'disabled')

    def load(self, name_inc):

        """
        Load extensions for the interface on activity;
        the extensions in service!.

                            Params

        name_inc: Name of the interface on activity; type str.
        """

        s_path.append(self.pack_name())
        exts = {}
        l_ext = self.__read(self.__list_extensions)
        st_ext = self.__read(self.__states_extensions)
        
        if st_ext == {}:
            st_ext = self.state_extensions()

        for category in [name_inc, 'all']:
            if category in l_ext:
                exts.update(l_ext[category])
        
        result = {}
        for path in exts:
            # _type = exts['type']
            n_ext = {'path': exts[path]}

            # Verify good state of the extension.
            read = self.__metadata(self.__read(exts[path] + '/extension.yml'))
            
            if isinstance(read, bool):  # Extencion not found.
                continue

            n_ext.update(read)
            _type = n_ext['type']
            r_name = n_ext['real name']
            
            del n_ext['type'], n_ext['real name']
            
            if _type in result:
                result[_type].update({r_name: n_ext})
                
            else:
                result.update({_type: {r_name: n_ext}})
            
            if r_name not in st_ext['disabled']:
                st_ext['enabled'].update({r_name: _type})
        
        self.__info_extensions.update(result)
        
        self.__state_extensions = st_ext
        self.__dump(self.__states_extensions, st_ext)

    def __metadata(self, body):
        """
        Alias: is_extencion?
        Inspect data and return false is not satisfied the 
        requirements for be a extencion else return an extencion.

                        Param

        body: A extencion; type: Dict.
        """

        anatomic = {
            'name': {'level': '!'},
            'real name': {'level': '!'},
            'call to': {'level': '#', 'type': 'theme'},
            'version': {'level': '!'},
            'author': {'level': '!', 'remplaces': ['maintainer', 'maintainers',
                                                   'authors']},
            'author email': {'level': '#', 'remplaces': ['maintainer email',
                                         'maintainers email', 'authors email']},
            'description': {'level': '#'},
            'dependencies': {'level': '#'},
            'license': {'level': '!'},
            'state': {'level': '!'},
            'main file': {'level': '!'},
            # In development.
            'interface': {'level': '!', 'values': ['commands', 'console',
                                                   'graphic', 'all']},
            'type': {'level': '!'}}

        for caracteristic in anatomic:

            if caracteristic not in body:
                interrupted = True

                if 'remplaces' in anatomic[caracteristic]:
                    for find_rs in anatomic[caracteristic]['remplaces']:
                        if find_rs in body:
                            if body[find_rs]:
                                interrupted = False
                                break

                elif anatomic[caracteristic]['level'] == '#':
                    interrupted = False

                if interrupted:
                    return not interrupted

            if 'values' in anatomic[caracteristic]:
                if not body[caracteristic] in anatomic[caracteristic]['values']:
                    return False

            if 'type' in anatomic[caracteristic] and caracteristic not in body:
                if body['type'] == anatomic[caracteristic]['type']:
                    body[caracteristic] = body['name']

        return body

    def pack_name(self, name=''):
        """Return: New Path of the in packages extencion."""
        return f"{self.__pack_dir}/{name}"
    
    def search(self, _type, rang='all', what='', exclude=True, state=False,
               only_result=True):
        """
        Return data of list of the extencions.

                            Params

        exclude: Exclude extensions desablers.
        state: Return result with the extencion state.
        """

        def if_less(cons, n1, n2):
            if n2:
                return cons[n1][n2]
            
            elif rang in n1:
                return cons[n1]
            
            else:
                return None

        result = []
        
        if _type == 'all':
            result = {}

            if state:
                for x_type in self.info_extensions:
                    for ste in self.info_extensions[x_type]:

                        if ste in self.__state_extensions['disabled']:
                            st = 'disabled'
                        
                        elif ste in self.__state_extensions['enabled']:
                            st = 'enabled'

                        n_x_type = f"{st} {x_type}"

                        if n_x_type in result:
                            result[n_x_type].update({ste:
                                             self.info_extensions[x_type][ste]})      
                        else:
                            result[n_x_type] = {ste:
                                             self.info_extensions[x_type][ste]}
                return result
            else:
                raise NameError('Your search in info_extensions.')

        find = self.info_extensions[_type]
        st = ''
        
        if rang != 'all':
            if exclude and rang in self.__state_extensions['disabled']:
                return
            
            result = if_less(find, rang, what)

            if state:

                if rang in self.__state_extensions['disabled']:
                    st = 'disabled'
                
                elif rang in self.__state_extensions['enabled']:
                    st = 'enabled'
                
                if st:
                    result = [st, result]
                else:
                    raise NameError(f"{rang} not in extencions")

            return result

        for ex in find:

            if exclude and ex in self.__state_extensions['disabled']:
                continue
            
            if only_result:
                result.append(if_less(find, ex, what))
            else:
                result.append({ex: if_less(find, ex, what)})
        
        return result

    @staticmethod
    def __thread(target, *args):
        td = Thread(target=target, args=args)
        td.start()
        td.join()

    def __install_zip(self, path):
        from zipfile import ZipFile

        zfile = ZipFile(path)
        if 'extencion.yml' in zfile.namelist():
            verify = self.__metadata(self.__read(zfile.read('extencion.yml')))

            if verify:
                self.__thread(zfile.extractall,
                              self.pack_name(verify['real name']))

                zfile.close()
                remove(path)
                return verify

        zfile.close()
        return True

    def __install_dir(self, path):
        verify = self.__metadata(self.__read(path))
        if verify:
            main_path = dirname(path)
            self.__thread(move, main_path,
                          self.pack_name(verify['real name']))
            return verify
        return True

    def __save_extencion(self, func, path):
        ext = func(path)

        if isinstance(ext, bool):
            return ext

        yaml_append(self.__list_extensions, {ext['real name']:
                  self.pack_name(ext['real name'])}, seccion=ext['interface'])
        return False

    def install(self, path):
        error = False

        if isdir(path):
            if 'extencion.yml' in listdir(path):
                path = join(path, 'extencion.yml')

        if path.endswith('extencion.yml'):
            error = self.__save_extencion(self.__install_dir, path)

        elif path.endswith('.zip'):
            error = self.__save_extencion(self.__install_zip, path)

        if error:
            exit("Error xxx")