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

    def __init__(self, **keywords):
        """Initialize interface selected for the user."""
        # Generic name for Console or Graphic Interface.
        
        self.interface = interface(**keywords)

    def mainloop(self):
        """The main loop (the live of this app)."""
        self.interface.mainloop()
        
def main(args=None):
    
    init_app(__name__, {}, 
               NAME, {'Mouse': 8},
             version=VERSION, author=AUTHOR, author_email=AUTHOR_EMAIL,
             description=DESCRIPTION, branch=BRANCH, _license=LICENSE, 
             repository=REPOSITORY, _copyright=COPYRIGHT, commit=COMMIT)
    
    args = manager_parse(args) if isinstance(args, list) else manager_parse()
    args['name'] = args['mode']
    del args['mode']
    app = OpenTranslation(**args)
    app.mainloop()


if __name__ == "__main__":
    main()