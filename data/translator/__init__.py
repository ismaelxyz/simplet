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
Script Name: translator/__init__.py
System of translation for OT.
"""

import requests
from data.utilities import read_file_error
from .record import Record


class Translator(object):

    """A translator of text and files."""

    def __init__(self, source, target, headers, url):
        self.source = source # from / oringin
        self.target = target # to / result
        self.headers = headers
        self.url = url
        
        self.__record = Record()

    def del_histori(self, number):
        """Delete an element of record."""

        if self.__record.include(number):
            self.__record.del_histori(number)
            return f"Del item: {self.__record.del_histori(number)} of hostori."
        return f'History not include: {number}.'

    def see_all(self):
        """Show all record."""

        return f"{self.__record.get_list()}"

    def size(self):
        """Return length of the record."""

        return f"{self.__record.size()}"

    def __save_data(self, text, trans, status_code):
        self.__record.update(self.url, self.source, self.target, text, trans,
                              self.headers, status_code)

    def translate(self, text):
        """Translate a text and save result in the record."""

        try:
            response = requests.post(self.url, data={'sl': self.source,
            'tl': self.target, 'q': text}, headers=self.headers)
            # 'fr' 'zh' 'en' 'es'
            # 

            if response.status_code == 200:
                # ['sentences']['trans']
                """
                {'sentences': [{'trans': 'l', 'orig': 'l', 'backend': 3, 'model_specification': [{}], 'translation_engine_debug_info': [{'model_tracking': {'checkpoint_md5': 'aab3c953a26de45c250412c67b4e9adb', 'launch_doc': 'tea_es_en_2019q4.md'}}]}], 'src': 'es', 'confidence': 0.0, 'spell': {}, 'ld_result': {'srclangs': ['es'], 'srclangs_confidences': [0.0], 'extended_srclangs': ['es']}}
                """
                result = response.json()
                if 'sentences' in result:
                    result = result['sentences'][0]['trans']
                    # result <- resultado
                    self.__save_data(text, result, response.status_code)
                    return result
                return ''

            else:
                print("not translate")
                # Error: traducción no realizada, estado del codigo: 150.
                info = ("Translation not done, code status: "
                         f"{response.status_code}.")
                self.__save_data(text, info, response.status_code)
                return [info]

        except requests.exceptions.ConnectionError:
            return ["Error: not connecting."]

        except requests.exceptions.Timeout:
            return ["Error: timeout."]
        
        except requests.exceptions.HTTPError:
            return ["Error: Your HTTP not exist."]

    def search(self, _id='last', data='[end_text]', other_data=''):
        """Find in the reccord."""

        return self.__record.search(_id, data, other_data)

    def save_translation(self, data, name_file='out.tc'):
        data = self.translate(data)
        if not isinstance(data, list):
            with open(name_file, 'a') as file:
                # por si es traducido de un texto y no de un archivo
                if data[-1] != "\n": data += "\n"
                file.write(data)
                file.close()
        return data

    def file_translate(self, name_file, out_file=''):
        """
        Translate a file, if out_file save translation file.
        
                                         Params
        name_file: File to translate.
        out_file: File of out result.
        """
        
        data = read_file_error(name_file)
        
        if isinstance(data, str):
            # File exist.
            if out_file:
                # Translate File and save result.
                return self.save_translation(data, out_file)
            else:
                # Translate File.
                return self.translate(data)
        else:
            # File not exist.
            return data