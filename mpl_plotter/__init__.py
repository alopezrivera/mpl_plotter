# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import re
import matplotlib as mpl
from matplotlib import font_manager


"""
Global variables
"""

__version__ = "5.5.0"

"""
General utilities
"""


def figure(figsize=(6, 6), backend='Qt5Agg'):
    """
    Create a Matplotlib figure with a given backend.
    Importantly, the backend is set BEFORE importing
    Pyplot.

    :param figsize: Matplotlib figure size. Default: (6, 6)
    :param backend: Matplotlib backend to be used. Default: 'Qt5Agg'

    :type figsize: tuple
    :type backend: str

    :return: Figure object
    """
    if not isinstance(backend, type(None)):
        mpl.use(backend)
    import matplotlib.pyplot as plt
    return plt.figure(figsize=figsize)


def get_available_fonts(silent=False):
    """
    Print all fonts available to Matplotlib in your system.
    """
    
    fnames = font_manager.get_font_names()
    
    if not silent:
        print("\n=============================")
        print("Fonts available to Matplotlib")
        print("=============================\n")
        for i in range(len(fnames)):
            n       = f'{i+1}'
            numeral = f'{n}.{" "*(len(str(len(fnames))) + 1 - len(n))}'
            print(f'{numeral}"{fnames[i]}"')

    return fnames


class markers:
    circle          = "o"
    x               = "x"
    thin_diamond    = "d"
    triangle_down   = "v"
    pentagon        = "p"
    vline           = "|"
    hline           = "_"
    # Decent
    point           = "."
    square          = "s"
    plus            = "+"
    triangle_up     = "^"
    triangle_left   = "<"
    triangle_right  = ">"
    tri_down        = "1"
    tri_up          = "2"
    tri_left        = "3"
    tri_right       = "4"
    octagon         = "8"
    hexagon1        = "h"
    hexagon2        = "H"
    diamond         = "D"
    tickleft        = 0
    tickright       = 1
    tickup          = 2
    tickdown        = 3
    caretleft       = 4
    caretright      = 5
    caretup         = 6
    caretdown       = 7
    caretleft_base  = 8
    caretright_base = 9
    caretup_base    = 10
    caretdown_base  = 11
    # Wonky tier
    plus_filled     = "P"
    star            = "*"
    # Garbage tier
    pixel           = ","

    # Icompatible
    incompatible    = [x]

    def __init__(self, hollow=False, plotter='plot'):
        """
        Markers class
        =============
        """
        self.hollow  = hollow
        self.plotter = plotter

        assert self.plotter in ['plot', 'scatter'], \
            "Plotter must be either 'plot' (for plt.plot, ax.scatter) or 'scatter' (plt.scatter)"

    def __getitem__(self, item):

        special = r'^__(.*?)\__$'

        m       = {k: markers.__dict__[k] for k in markers.__dict__.keys() if (self.hollow and k not in self.incompatible) or not self.hollow}
        keys    = [k for k in m.keys() if not re.match(special, k)]
        marker  = {'marker': m[keys[item]]}

        if self.hollow:
            if self.plotter == 'scatter':
                marker['mfc']        = 'none'
            else:
                marker['facecolors'] = 'none'

        return marker
