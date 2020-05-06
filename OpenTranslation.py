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
Name: Open Translation.
Alias: OT.
Script Name: OpenTranslation.py
A Translate for all persons, in evolution (Main file).
"""

from data import interface
from data.parse import manager_parse
from data.constans import AUTHOR, AUTHOR_EMAIL, BRANCH, LICENSE, REPOSITORY, \
    COMMIT, COPYRIGHT, NAME, DESCRIPTION, VERSION
from otapplication import init_app


class OpenTranslation():

    """ The face of Open Translation. The Open Translation at all
    persons in evolution.
    """

    def __init__(self):
        """Initialize interface selected for the user."""
        # Generic name for Console or Graphic Interface.
        
        keywords = manager_parse()
        keywords['name'] = keywords['mode']
        del keywords['mode']
        self.interface = interface(**keywords)

    def mainloop(self):
        """The main loop (the live of this app)."""
        self.interface.mainloop()

def run(func):
    # Decorator
    return func()

# The main function of OT (Only One).
@run
def main(name=__name__):
    import py
    init_app(name, {}, 
               NAME, {'vaca': 8},
             version=VERSION, author=AUTHOR, author_email=AUTHOR_EMAIL,
             description=DESCRIPTION, branch=BRANCH, _license=LICENSE, 
             repository=REPOSITORY, _copyright=COPYRIGHT, commit=COMMIT)
    
    app = OpenTranslation()
    app.mainloop()