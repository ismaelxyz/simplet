import cairosvg
from sys import argv

name = argv[1]

with open(f"{name}.svg", 'rb') as file:
  png = cairosvg.svg2png(file_obj=file)

with open(f"{name}.png", 'wb') as file:
  file.write(png)
