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
Script Name: checkconnection.py
Check connection in your computer.
"""

def check_connection(url: str='https://github.com') -> str:
    from requests import get
    try:
         __import__('requests').get(url, timeout=60)
         return 'Establish.'
        
    except:
        return 'Not establish.'


if __name__ == "__main__":
    print(check_connection())