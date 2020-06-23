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
Script Name: windows.py
Graphic support for OT graphic interface.
"""

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from .menu import OTMenu
from .boxcenter import BoxCenter
from .combobox import OTBCombobox
#from .statusbar import OTSB  # Class
from .topconf import TopConf
from .about import TopAbout
from data.utilities import find_with_glob
from tkinter import PhotoImage
from os.path import join


# NOTE: Tk is Windows in this Project.
class OTWindows(Tk):
    # This is a superclass only use whit subclass.

    def __init__(self):
        
        super().__init__()
        self.tk.createcommand('find_with_glob', find_with_glob)
        self.tk.eval("source data/otgraphic/windows.tcl")
        self.tk.eval(f"create_logo {self}")
        
        # FIXME: If your see this color in the windows OT Failure.
        self['background'] = 'red'
        # ('All Files', '*.*')
        self.__ftypes = [('TCFile', '*.cr;*.tc'), ('Plain Text', '*.txt')]
    
    def create_default_commands(self):
        # This is for Tk

        # Crate function for TopAbout
        img_load = find_with_glob('data+otgraphic','*load_image.tcl', True)[0]
        self.tk.eval('source %s' % img_load)

        # Complete in SubClass exception find_with_glob.

    def start(self):

        self.load_menu()
        self.load_idiom_area()
        self.load_box_center()
        self.load_statusbar()

        # Text widgets
        self.translate = self.box_center.text_translate
        self.translation = self.box_center.text_translation

    def load_idiom_area(self):
        self.combobox = OTBCombobox(self)
        self.combobox.start()

    def load_menu(self):
        self.menu = OTMenu(self)
        self.menu.start()

    def load_box_center(self):
      self.box_center = BoxCenter(self)
      self.box_center.start()

    def load_statusbar(self):
        
        self.tk.call("source", find_with_glob('data+otgraphic', '*statusbar.tcl', True)[0])
        self.tk.eval("statusbar_start")

    def save_result(self) -> str:
        return asksaveasfilename(filetypes=self.__ftypes)

    def tranlate_file(self) -> str:
        return askopenfilename(filetypes=self.__ftypes)

    def save_tranlate_file(self) -> str:
        return [askopenfilename(filetypes=self.__ftypes),
               asksaveasfilename(filetypes=self.__ftypes)]
    
    def top_conf(self):
        TopConf(self)
    
    def top_about(self):
        TopAbout(self)