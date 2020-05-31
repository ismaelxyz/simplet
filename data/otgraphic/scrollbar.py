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


# Script Name: scrollbar.py

from tkinter.ttk import Scrollbar

class OTScrollbar(Scrollbar):
    
    def set(self, first, last):
        # Set the fractional values of the slider position (upper and
        # lower ends as value between 0 and 1).
        self.tk.call(self._w, 'set', first, last)

# XXX: In develop.
# __END__
class AutoHideScrollbar(OTScrollbar):
    # Scrollbar that automatically hides when not needed.
    
    def __init__(self, master, **kwargs):
        # Create a Scrollbar.

        super().__init__(master, **kwargs)
        self._pack_kw = {}
        self._place_kw = {}
        self._layout = 'place'

    def set(self, lo, hi):
        """
        Set the fractional values of the slider position.
        
        :param lo: lower end of the scrollbar (between 0 and 1)
        :type lo: float
        :param hi: upper end of the scrollbar (between 0 and 1)
        :type hi: float
        """
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            if self._layout == 'place':
                self.place_forget()
            elif self._layout == 'pack':
                self.pack_forget()
            else:
                self.grid_remove()
        else:
            if self._layout == 'place':
                self.place(**self._place_kw)
            elif self._layout == 'pack':
                self.pack(**self._pack_kw)
            else:
                self.grid()
        super().set(lo, hi)

    def _get_info(self, layout):
        # Alternative to pack_info and place_info in case of bug.
        info = str(self.tk.call(layout, 'info', self._w)).split("-")
        dic = {}
        for i in info:
            if i:
                key, val = i.strip().split()
                dic[key] = val
        return dic

    def place(self, **kw):
        
        super().place(**kw)
        self._place_kw = self._get_info("place")
        self._layout = 'place'

    def pack(self, **kw):

        super().pack(**kw)
        self._pack_kw = self._get_info("pack")
        self._layout = 'pack'

    def grid(self, **kw):
        print(self, kw)
        super().grid(**kw)
        self._layout = 'grid'

del AutoHideScrollbar