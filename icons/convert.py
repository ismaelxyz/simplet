"""
  WARNING: This script is deprecated, use `cairosvg` command line instead
"""

import cairosvg
from sys import argv

def main():
  """ Convert a image from SVG to PNG format """

  name = argv[1]
  output = argv[1]

  if len(argv) >= 2:
    output = argv[2]  

  if name.endswith('.svg')
    name += '.svg'

  if output.endswith('.png')
    output += '.png'

  with open(f"{name}", 'rb') as file:
    png = cairosvg.svg2png(file_obj=file)

  with open(f"{output}", 'wb') as file:
    file.write(png)


if __name__ == '__main__':
  main()