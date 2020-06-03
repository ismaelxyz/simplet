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


# Script Name: statusbar.tcl

# source statusbar.tcl

# -XXX: Tk/Ttk Commands: winfo wm destoy :XXX-

# class StatusBar(Frame):

# Attributes of class OTStatusbar.

variable list_childres { }

# methods
proc create_sbar { } {
    if {!([winfo exist .statusbar])} {
        ttk::frame .statusbar
        pack .statusbar -fill x -side bottom
    }
}

proc add_label {name {txt ""}} {
    global list_childres
    
    if {!($name in $list_childres)} {
        ttk::label .statusbar.$name -text $txt
        pack .statusbar.$name -side right -padx 2
        lappend list_childres $name
    }
}

proc set_label {name text} {
    global list_childres

    if {$name in $list_childres} {
        .statusbar.$name configure -text $text
    }
}

proc destroy_label {name} {
    global list_childres

    if {$name in $list_childres} {
        destroy .statusbar.$name
    }
}

proc show_message {text {time 2000}} {
    proc clear_messages {} {
    set_label message ""
    }

    set_label message "Message: $text"
    after $time clear_messages
}

proc confirm_connectivity {} {
    set_label connection "Connection: [check_connection]"
}

proc statusbar_start {} {
    create_sbar
    add_label message
    show_message Welcome 4000
    add_label connection
    confirm_connectivity
}