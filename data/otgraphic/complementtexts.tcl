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


# Script Name: complementtexts.py

# Complement for translate and translation widget.

namespace eval text_ton {
  # Alias: OT text of translation complement.
  # Complement for translation widget.

  proc insert_text {text} {
    # Clean at insert new text in the widget of translation.
    change_state "normal"
    .!boxcenter.!panedwindow.!frame2.!ottext delete "1.0" "end"
    tk::TextInsert .!boxcenter.!panedwindow.!frame2.!ottext $text
    change_state "disable"
    return
  }

  proc change_state {state} {
    # Change state of widget !ottext.
    .!boxcenter.!panedwindow.!frame2.!ottext configure -state $state
    return
  }
}

namespace eval text_tle {
  # Alias: OT text of translate complement.
  # Complement for translate widget.

  proc see_text {} {
    # See text in the widget of translate.   
    return [.!boxcenter.!panedwindow.!frame.!ottext get "1.0" "end"]
  }
}