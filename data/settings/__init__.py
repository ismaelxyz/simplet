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


# Script Name: settings/__init__.py

__all__ = ['get_idioms', 'del_idioms', 'add_idioms', 'init_settings', 'os_info',
           'get_setting', 'set_setting', 'sync_settings', 'sync_idioms']

from os.path import isfile
from data.utilities import yaml_append, yaml_dump, yaml_load_except

# State init of idioms and settings in OT.
idioms = ['en', 'es']
settings = {
    'arrow': '->',
    'language': 'English',
    'source': 'es',
    'target': 'en',
    'theme': 'default',
    'headers': {'Charset': 'UTF-8',
                'User-Agent': 'AndroidTranslate/5.3.0.RC02.130475354-'
                '53000263 5.1 phone TRANSLATE_OPM5_TEST_1'},
    'url': 'https://translate.google.com/translate_a/single?client=at&d'
    't=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=es-ES&ie=UTF-8&oe=UTF-'
    '8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e'
}


# https://translate.google.com/#view=home&op=translate&sl=es&tl=pt&text=a
def sync_idioms():
    # Sync idioms app whit idioms user.
    global idioms
    idioms = yaml_append(os_info('Con OT') + '/listidioms.yml', idioms, re=True,
                         _type=[])

def sync_settings():
    # Sync settings app whit settings user.
    global settings
    sett = yaml_load_except(os_info('Con OT') + '/settings.yml')
    settings.update(sett)

def get_idioms():
    # Get all idioms in storage.
    return idioms.copy()

def del_idioms(*args):
    #  Del idioms of the app.
    global idioms

    data = yaml_load_except(os_info('Con OT') + '/listidioms.yml', [])
    for x in args:
        if x in data:
            data.remove(x)
    yaml_dump(os_info('Con OT') + '/listidioms.yml', data)

    idioms = data

def add_idioms(*args):
    #  Add idioms to the app.
    global idioms

    for x in args:
        if x not in idioms:
            idioms.append(x)
    yaml_dump(os_info('Con OT') + '/listidioms.yml', idioms)

def get_setting(*args):
    #  Get setting of the interaction.
    data = []
    for x in args:
        if x in settings:
            data.append(settings[x])
    return data if len(data) > 1 else data[0]

def set_setting(keyward):
    #  Set a data setting of the app.
    global settings
    settings = yaml_append(os_info('Con OT') + '/settings.yml', keyward, re=True)

os_info = None

def init_settings():
    from .osinfo import OsInfo
    from data.utilities import force_path

    global os_info

    os_info = OsInfo()
    # Start configure necessary for init of OT.
    home_ot = os_info.get('Home OT')

    # Paths special.
    px = home_ot + '/extensions'
    c = home_ot + '/config'

    # Create special path if not exist.
    force_path(c, px)

    os_info.add(con_ot=c, home_ext=px)

    # Dir config ot for user.
    info_app = {}
    from data import constans
    for x in dir(constans):
        if '_' not in x:
            info_app[x] = getattr(constans, x)

    os_info.add(**info_app)
    del constans, info_app, c

    # Occulter unnecessary info.
    os_info = os_info.get
    # Sync data.
    sync_idioms()
    sync_settings()

    # Implement del for librate memory.
    #del init_settings, isfile, work_files, sync_settings, sync_idioms
    return os_info