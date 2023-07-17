# SVG Badge Generator

This project provides Python scripts to generate SVG badges with customizable text, color, and FontAwesome icons.

## Features

* Resizes and recolors SVG icons.
* Fetches SVG icons from the GitHub FontAwesome library.
* Generates badges with the given specifications including text, color, and optional FontAwesome icons.

## Functions

### `resize_and_recolor_svg(svg_data, new_size=12, new_color="#000")`

This function takes in original SVG data and resizes and recolors it. The new size and color can be specified as parameters. By default, the new size is set to 12 and the color is set to black ("#000").

### `embed_svg_icon(icon_name, color)`

This function fetches an SVG icon by its name from the GitHub FontAwesome library. The icon is then resized and recolored before being returned as a string.

### `draw_svg(text1, text1_color, color1, text2, text2_color, color2, modifier1="", modifier2="", modifier3="", icon_name="")`

This function creates a badge SVG with the given specifications. The badge consists of two parts, each with its own text, text color, and background color. Additional modifications can be made to the badge. If the name of an icon is provided, the icon will be displayed in the first part of the badge.

## Usage

To use the SVG Badge Maker, import the functions from the Python file and call them with the appropriate parameters. See the docstrings in the code for more information on the parameters of each function.

## Dependencies

* `requests` for fetching SVG icons.
* `drawsvg` for creating and manipulating SVG data.
* `base64` for encoding the font file.
* `xml.dom.minidom` for parsing SVG data.

## Note

This project fetches icons from the [GitHub FontAwesome library](https://github.com/FortAwesome/Font-Awesome). Ensure that you have a working internet connection when running this project.