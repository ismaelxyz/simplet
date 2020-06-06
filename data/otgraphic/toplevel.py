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
Script Name: toplevel.py
Support of toplevel for OTGraphic.
"""

from tkinter import Toplevel
from data.utilities import yaml_load_except, force_path, yaml_dump, yaml_append

class OTToplevel(Toplevel):

    def __init__(self, master, title: str):
        
        super().__init__(master)
        self.title('Open Translation: ' + title)
        self.grab_set()
        self.transient(master=master)
        self.tk.eval(f"create_logo {self}")
        
        # Create main dir (Of TofConf) if not exist and sync conf.
        self._home = self.master.consult_user('Home OT') + '/tops'
        self._file_conf = self._home + '/settings.yml'
        force_path(self._home)

        # XXX: Formule deficient in full screen.
        size = lambda x: int(x) - int(int(x) * 0.06)
        
        loc_x = lambda x, x2: int(int(x) * 0.03) + int(x2)
        loc_y = lambda x, x2: int(int(x) * 0.045) + int(x2)
        
        a, b = self.master.geometry().split('x')
        b, c, d = b.split('+')
        self.geometry(f"{size(a)}x{size(b)}+{loc_x(a, c)}+{loc_y(b, d)}")
        
        # Vars for subclass.
        self.screens, self._config, self.__screen  = {}, {}, ''
    
    def opack(self, obj, **kw):
        obj.pack(**kw)

    def set_configuration(self, name: str, value):
        raise NotImplementedError("This method is for subclasses.")

    def _clear_screen(self, screen: str, clear: bool=True):
        """
        Control of screen for interactives toplevels.
        XXX: Please Use with caption.
        """

        if self.__screen != screen:
            self.__screen = screen
            self.set_configuration('screen', screen)
            if clear:
                for x in self.children.copy():
                    if x != 'left': self.children[x].destroy()
            return True
        return False
    
    def _sync_conf(self, seccion: str):
        """Sync configuration in the topslevels"""
        cong = yaml_load_except(self._file_conf, _type={})
        if seccion in cong:
            self._config.update(cong[seccion])
    
    def destroy(self, seccion: str):
        """Save config and delete widget."""
        yaml_append(self._file_conf, self._config, seccion)
        super().destroy()