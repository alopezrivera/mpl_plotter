# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only


"""
.. include:: ./documentation.md
"""

import re
import matplotlib as mpl
import matplotlib.font_manager

from alexandria.shell import print_color


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


def get_available_fonts():
    """
    Print all fonts available to Matplotlib in your system.
    """
    flist = matplotlib.font_manager.get_fontconfig_fonts()
    names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]

    print_color("Matplotlib: available fonts", "blue")
    for i in range(len(names)):
        n = f"{i+1}"
        numeral = n + "." + " "*(4-len(n))
        print(numeral+'"'+names[i]+'"')


# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Huracan utilities
-----------------
"""

import re
import sys
import inspect


def setattr_namespace(o, namespace):
    """
    Set all variables declared in a namespace as as attributes
    of a class instance.
    ---

    1. Obtain list of module names
    2. Get namespace variables
       - Discard all variables with names starting and ending with '_'
    3. Create a dictionary of namespace variable names and values
    4. Set namespace variables as attributes of the input object
       - Given class instance _o_ will not set as attribute of itself
       - The parent class of _o_ will not be set as an attribute of _o_
         if present in the provided namespace.

    :param o: Instance of any given class.
    :param namespace: A given namespace.
                      - locals()
                      - globals()

    :type o: object
    :type namespace: dict
    """
    # List of module names
    _mods_ = list(set(sys.modules) & set(namespace))
    # List of function arguments
    _args_ = setattr_namespace.__code__.co_varnames
    # Get namespace variables:
    #    List of local variables which are not special variables nor module names
    keys = [key for key in namespace.keys() if (key[0] != '_' and key[-1] != '_') and key not in _mods_]
    # Dictionary of namespace variable names and values
    vars = {key: namespace[key] for key in keys}
    for key, value in vars.items():
        if not type(value) == type(o)\
                and not isinstance(o, value if inspect.isclass(value) else type(value)):  # Avoid _o_, parent of _o_
            # Set namespace variables as attributes of the input object
            setattr(o, key, value)


class markers:
    """
    Markers class
    -------------
    """
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


