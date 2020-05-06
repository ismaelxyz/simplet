proc display_logo {path} {
  image create photo ::img::logo -format PNG -file $path
  .!topabout.!frame.logo configure -image ::img::logo
} 