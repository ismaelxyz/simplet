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


from ..combobox import OTACombobox

"""
Script Name: topbox.py

"""


class TopCombobox(OTACombobox):

    def __init__(self, master, key, call_to, completevalues=None, sync=False,
                 **kwargs):
        super().__init__(master, completevalues, sync, **kwargs)
        self.__key = key
        self.__call_to = call_to

    def _comfirm_text(self, even):
        text = self.view_text
        super()._comfirm_text(even)
        
        if text != self.get() and self.get() in list(self.values):
            self.__call_to.set_configuration(self.__key, self.get())
