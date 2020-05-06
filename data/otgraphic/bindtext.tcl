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


# Script Name: bindtext.py

# Encargado de ejecutar la traducción y mostrarla en pantalla.
# find_with_glob: Python's function.
source [lindex [find_with_glob data *otgraphic/complementtexts.tcl true "\ "] 0]

# Warning: bind not failed if inside it ocurred an error.
# Acvertencia: bind no falla si dentro de el ocurre un error.

variable text ""

bind .!boxcenter.!panedwindow.!frame.!ottext <KeyPress> {
  # Capture text.
  variable text [text_tle::see_text]
}

bind .!boxcenter.!panedwindow.!frame.!ottext <KeyRelease> {
  # Compare text origin whit final.
  # If diferent.
  if {[string compare $text [text_tle::see_text]]} {
    # Function of Python (do_translation: translatation).
    variable new_text [do_translation [text_tle::see_text]]
    
    if {[string length $new_text]} {
      text_ton::insert_text $new_text
    }
  }
  variable text ""
}