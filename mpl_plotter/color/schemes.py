# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Color schemes
-------------
"""


from matplotlib.colors import LinearSegmentedColormap


def colorscheme_one():
    custom = ["darkred",
              "#1f8fff",
              "#FF8F1F",
              "#00C298",
              "#FFBD00",
              "#00FFC4",
              "#FF003B"]
    tableau = ['tab:blue',
               'tab:orange',
               'tab:green',
               'tab:red',
               'tab:purple',
               'tab:brown',
               'tab:pink',
               'tab:gray',
               'tab:olive',
               'tab:cyan']
    return custom + tableau


def custom(red, green, blue,
           name="coolheat", n=1024):
    """
    :param red: List of (red fraction, y0, y1) tuples
    :param green: List of (red fraction, y0, y1)
    :param blue: List of (red fraction, y0, y1)
    :param name: Colormap name
    :param n: RBG quantization levels
    :return: Colormap
    """
    dictionary = {
        'red': red,
        'green': green,
        'blue': blue}
    return LinearSegmentedColormap(name, dictionary, n)
