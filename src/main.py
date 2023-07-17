import requests
import drawsvg as draw
import base64
from xml.dom import minidom


def resize_and_recolor_svg(svg_data, new_size=12, new_color="#000"):
    """
    Resizes and recolors a given SVG icon.

    :param svg_data: str - Original SVG data
    :param new_size: int - New size for the SVG icon. Default is 12.
    :param new_color: str - New color for the SVG icon. Default is #000 (black).
    :return: str - Updated SVG data.
    """
    doc = minidom.parseString(svg_data)  # Parse the SVG data using minidom

    # Resize the SVG
    svg_element = doc.getElementsByTagName('svg')[0]
    svg_element.setAttribute('width', str(new_size))
    svg_element.setAttribute('height', str(new_size))

    # Change the color of the SVG
    all_paths = doc.getElementsByTagName('path')
    for path in all_paths:
        path.setAttribute('fill', new_color)

    return svg_element.toxml()


def embed_svg_icon(icon_name, color):
    """
    Fetches an SVG icon by name from the GitHub FontAwesome library
    and returns it as a string after resizing and recoloring.

    :param icon_name: str - Name of the icon to be fetched.
    :param color: str - Color to be applied to the icon.
    :return: str - SVG data of the fetched icon.
    """
    solid_url = f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/{icon_name}.svg"
    regular_url = f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/regular/{icon_name}.svg"
    brands_url = f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/brands/{icon_name}.svg"

    response = requests.get(solid_url)

    # Check if the request was successful
    if response.status_code == 200:
        return resize_and_recolor_svg(response.text, 12, color)
    else:
        response = requests.get(regular_url)

        if response.status_code == 200:
            return resize_and_recolor_svg(response.text, 12, color)
        else:
            response = requests.get(brands_url)

            if response.status_code == 200:
                return resize_and_recolor_svg(response.text, 12, color)

            else:
                raise Exception(f"Could not fetch the icon '{icon_name}'. Please make sure the icon name is correct.")


def draw_svg(text1, text1_color, color1, text2, text2_color, color2,
             modifier1="", modifier2="", modifier3="", icon_name=""):
    """
    Creates a badge SVG with the given specifications.

    :param text1: str - Text to be displayed in the first part of the badge.
    :param text1_color: str - Color of the first text.
    :param color1: str - Background color of the first part of the badge.
    :param text2: str - Text to be displayed in the second part of the badge.
    :param text2_color: str - Color of the second text.
    :param color2: str - Background color of the second part of the badge.
    :param modifier1: str - Additional modification for the badge. Default is "".
    :param modifier2: str - Additional modification for the badge. Default is "".
    :param modifier3: str - Additional modification for the badge. Default is "".
    :param icon_name: str - Name of the icon to be displayed in the first part of the badge. Default is "".
    """
    # Define dimensions
    shield_height = 20
    corner_radius = 4
    font_size = 12
    padding = 10
    estimated_char_width = font_size * 0.6

    # Define the icon width
    icon_width = 20 if icon_name else 0

    # Calculate shield widths
    text_width = len(text1) * estimated_char_width
    shield1_width = text_width + 2 * padding + icon_width
    text_width = len(text2) * estimated_char_width
    shield2_width = text_width + 2 * padding

    # Badge dimensions
    badge_width = icon_width + shield1_width + shield2_width

    # Create an SVG drawing
    d = draw.Drawing(badge_width, shield_height)

    # Append the font
    with open('assets/robotomono.woff2', 'rb') as font_file:
        font_base64 = base64.b64encode(font_file.read()).decode()

    # Embed the font in the SVG
    font_face = f"""
    <defs>
        <style>
            @font-face {{
                font-family: 'Roboto Mono';
                src: url(data:application/x-font-woff2;charset=utf-8;base64,{font_base64}) format('woff2');
            }}
        </style>
    </defs>
    """
    d.append(draw.Raw(font_face))

    # Create shield paths checking if 1 or 2 shields are needed
    # Define right_end for shield1 based on text2 presence
    right_end = f'H {shield1_width - corner_radius} ' \
                f'A {corner_radius},{corner_radius} 0 0,1 {shield1_width},{corner_radius} ' \
                f'V {shield_height - corner_radius} ' \
                f'A {corner_radius},{corner_radius} 0 0,1 {shield1_width - corner_radius},{shield_height} ' if not text2 else f'H {shield1_width}'

    path_data_shield_1 = f'M 0,{corner_radius} ' \
                         f'A {corner_radius},{corner_radius} 0 0,1 {corner_radius},0 ' \
                         f'{right_end} ' \
                         f'V {shield_height} ' \
                         f'H {corner_radius} ' \
                         f'A {corner_radius},{corner_radius} 0 0,1 0,{shield_height - corner_radius} ' \
                         f'Z'

    path_data_shield_2 = f'M 0,0 ' \
                         f'H {shield2_width - corner_radius} ' \
                         f'A {corner_radius},{corner_radius} 0 0,1 {shield2_width},{corner_radius} ' \
                         f'V {shield_height - corner_radius} ' \
                         f'A {corner_radius},{corner_radius} 0 0,1 {shield2_width - corner_radius},{shield_height} ' \
                         f'H 0 Z'

    # Draw shields
    shield1 = draw.Path(path_data_shield_1, fill=color1)
    shield2 = draw.Path(path_data_shield_2, fill=color2, transform=f"translate({shield1_width}, 0)")
    d.append(shield1)

    if text2:
        d.append(shield2)

    # Append icon to shield 1 if icon is supplied
    if icon_name:
        icon_svg = embed_svg_icon(icon_name, text1_color)
        d.append(draw.Raw(f'<g transform="translate(5,4)">{icon_svg}</g>'))

    # Draw texts
    text_distance_from_start = (shield1_width / 2) + 8 if icon_name else shield1_width / 2
    d.append(draw.Text(text1, 12, text_distance_from_start, shield_height / 2,
                       center=True, fill=text1_color, font_family='Roboto Mono'))

    if text2:
        d.append(
            draw.Text(text2, 12, (shield2_width / 2) + shield1_width, shield_height / 2, center=True, fill=text2_color,
                      font_family='Roboto Mono'))

    # Save the SVG
    d.save_svg("badge.svg")

# Example call
draw_svg("Carlos","#ffffff","#8855ff","","#ffffff","#aa77aa","","","","python")