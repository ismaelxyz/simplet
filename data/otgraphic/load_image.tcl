proc display_logo {path widget} {
  image create photo ::img::logo -format PNG -file $path
  $widget configure -image ::img::logo
} 