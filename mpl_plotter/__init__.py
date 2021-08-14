"""
.. include:: ./documentation.md
"""

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

