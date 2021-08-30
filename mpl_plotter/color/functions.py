import re
from matplotlib.colors import to_hex


def hex_to_rgb(color):
    """
    :type color: string
    """

    if not re.match("#([0-9a-fA-f]{2}){3}", color):
        color = to_hex(color)

    c = color[1:]
    return [int(re.match("[0-9a-fA-f]{2}", c[i:i+2]).string, 16) for i in range(0, len(c), 2)]


def rgb_to_hex(color):
    """
    :type color: list of int
    """
    r, g, b = color
    return f'#{r:02x}{g:02x}{b:02x}'


def complementary(color, fmt='hex'):
    """
    Return complementary of [R, G, B] or hex color.

    :param fmt:  Output format: 'hex' or 'rgb'.

    :type color: list of int or string
    :type fmt:   string
    """

    assert isinstance(color, list) or isinstance(color, str)

    if isinstance(color, list):
        comp = [255 - i for i in color]
    elif isinstance(color, str):
        comp = [255 - i for i in hex_to_rgb(color)]

    if fmt == 'hex':
        return rgb_to_hex(comp)
    elif fmt == 'rgb':
        return comp


def delta(color, factor, fmt='hex'):
    """
    Darker or lighten the input color by a percentage of
    <factor> ([-1, 1]) of the color spectrum (0-255).

    :param fmt:    Output format: 'hex' or 'rgb'.
    :param factor: [-1, 1] Measure in which the color will be modified.

    :type color:   list of int or string
    :type factor:  float
    :type fmt:     string
    """

    assert isinstance(color, list) or isinstance(color, str)

    if isinstance(color, list):
        c_mod = [min(max(0, int(i + factor*255)), 255) for i in color]
    elif isinstance(color, str):
        c_mod = [min(max(0, int(i + factor*255)), 255) for i in hex_to_rgb(color)]

    if fmt == 'hex':
        return rgb_to_hex(c_mod)
    elif fmt == 'rgb':
        return c_mod
