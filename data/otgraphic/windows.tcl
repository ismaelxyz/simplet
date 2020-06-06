wm title . "Open Translation"

proc create_logo {windows} {
    # Insert logo in the windows or Toplevel.
    
    image create photo ::img::otlogo -format PNG -file [lindex [find_with_glob \
    "data+otgraphic/images" "*logo13.png" " "] 0]
    wm iconphoto $windows ::img::otlogo
}

#############################

