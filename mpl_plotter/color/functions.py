# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Methods
-------
"""

import numpy as np
import matplotlib as mpl
from matplotlib.colors import to_hex, to_rgba


def complementary(color, fmt='hex'):
    """
    Return complementary of [R, G, B] or hex color.

    :param fmt:  Output format: 'hex' or 'rgb'.

    :type color: list of int or string
    :type fmt:   string
    """

    assert isinstance(color, list) or isinstance(color, tuple) or isinstance(color, str)

    if isinstance(color, list) or isinstance(color, tuple):
        comp = [(1 - i) for i in color]
    elif isinstance(color, str):
        comp = [(1 - i) for i in to_rgba(color, 1.0)]

    if fmt == 'hex':
        return to_hex(comp)
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

    assert isinstance(color, list) or isinstance(color, tuple) or isinstance(color, str)

    if isinstance(color, list) or isinstance(color, tuple):
        c_mod = [min(max(0, i + factor), 1) for i in color]
    elif isinstance(color, str):
        c_mod = [min(max(0, i + factor), 1) for i in to_rgba(color, 1.0)]

    if fmt == 'hex':
        return to_hex(c_mod)
    elif fmt == 'rgb':
        return c_mod
