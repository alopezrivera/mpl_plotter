# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Common
------
"""

import matplotlib as mpl

from mpl_plotter import figure

def method_backend(plot):

    # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
    # or matplotlib.backends is imported for the first time.

    if plot.backend is not None:
        try:
            mpl.use(plot.backend)
        except AttributeError:
            raise AttributeError('{} backend not supported with current Python configuration'.format(plot.backend))

def method_figure(plot):
    if plot.style is not None:
        plot.plt.style.use(plot.style)
    plot.fig = figure(figsize=plot.figsize)

def method_fonts(plot):
    """
    For context, Matplotlib's typesetting works as follows.

    * Five typeface families are defined: *serif*, *cursive*, *sans-serif*,
       *monospace* and *fantasy*.
    * Each family has a **list of typefaces** associated with it.
    * The user then chooses a family to typeset a plot, and the **first typeface**
       in the family's typeface list found in the user's system is used to do so.

    Matplotlib allows users to modify the **lists of typefaces** of each
    family through its `runtime configuration (rc) dictionary, ``matplotlib.rcParams`` <https://matplotlib.org/stable/tutorials/introductory/customizing.html>`_.
    This dictionary will be referred to as ``rcParams``.

    MPL Plotter sets lists of its own for each of the typeface families, as well as
    choosing a *default* and *fallback* typeface for math.
    
    The typesetting of text in MPL Plotter is defined by two parameters:
    
    * ``font``
    * ``font_math``

    Furthermore, MPL Plotter allows the user to set the default color for all text,
    including title, labels and floating text, with the parameter ``font_color``.
    
    **font**
    
    If the ``font`` attribute of the plot is **one of these families**,
    ``rcParams`` ``font.family`` entry will be set to ``plot.font``, thereby making
    the **first found typeface** of the ``plot.font`` *family* typeface list the
    chosen typeface for text in your plot.
    
    Otherwise, that is, if the ``font`` attribute of the plot is **not** one of the
    families, the provided ``font`` will be ``insert``ed to the *serif* family
    typeface list, and the ``rcParams`` ``font.family`` entry will be set to *serif*,
    thereby making the provided ``font`` the chosen typeface for text in the plot.

    **font_math**

    The ``font_math`` attribute of the plot determines the typeface used for math
    through the ``rcParams`` ``'mathtext.fontset`` entry, and it may take the following values:

    * ``cm`` (Computer Modern)
    * ``dejavusans``
    * ``dejavuserif``
    * ``stix``
    * ``stixsans``

    Lastly, Matplotlib allows users to choose the typeface of bold, calligraphic,
    italic and other highlight typefaces for rendered math. MPL Plotter does not
    provide an interface for this, but it can be done my manually setting the
    value of the following entries in ``rcParams``:
    
    * ``mathtext.bf``
    * ``mathtext.cal``
    * ``mathtext.it``
    * ``mathtext.rm``
    * ``mathtext.sf``
    * ``mathtext.tt``

    **font_color**
    
    The default text color, set through the ``rcParams`` ``text.color`` and
    ``axis.labelcolor`` entries, may be overridden, and MPL Plotter offers the
    ``title_color`` argument to that effect in the case of titles.
    To override the color of tick and axis labels or other text in a plot please
    consult the Matplotlib documentation. As long as you do **not** set ``show=True``
    in the call to an MPL Plotter plotting class, you are free to continue customization
    afterwards, including but not limited to text color.
    """

    # Defaults - Text
    mpl.rcParams['font.serif'] = [
        'DejaVu Serif',
        'Latin Modern Roman'
    ]
    mpl.rcParams['font.cursive'] = [
        'Apple Chancery'
    ]
    mpl.rcParams['font.sans-serif'] = [
        'DeJaVu'
    ]
    mpl.rcParams['font.monospace'] = [
        'Bitstream Vera Sans Mono'
    ]
    mpl.rcParams['font.fantasy'] = [
        'Chicago'
    ]

    # Defaults - Math
    mpl.rcParams['mathtext.fontset']  = 'cm'
    mpl.rcParams['mathtext.default']  = 'it'
    mpl.rcParams['mathtext.fallback'] = 'stix'


    # Configuration
    if plot.font in ['serif', 'cursive', 'sans-serif', 'monospace', 'fantasy']:
        mpl.rcParams['font.family'] = plot.font
    else:
        family   = 'serif'
        typeface = mpl.rcParams['font.serif'].insert(plot.font)

    # Color
    mpl.rcParams['text.color']      = plot.font_color
    mpl.rcParams['axes.labelcolor'] = plot.font_color

def method_workspace_style(plot):
    if plot.light:
        plot.workspace_color = 'black' if plot.workspace_color is None else plot.workspace_color
        plot.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if plot.workspace_color2 is None else plot.workspace_color2
        plot.style = 'classic'
    elif plot.dark:
        plot.workspace_color = 'white' if plot.workspace_color is None else plot.workspace_color
        plot.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if plot.workspace_color2 is None else plot.workspace_color2
        plot.style = 'dark_background'
    else:
        plot.workspace_color = 'black' if plot.workspace_color is None else plot.workspace_color
        plot.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if plot.workspace_color2 is None else plot.workspace_color2
        plot.style = None

def method_background_color(plot):
    plot.fig.patch.set_facecolor(plot.background_color_figure)
    plot.ax.set_facecolor(plot.background_color_plot)
    plot.ax.patch.set_alpha(plot.background_alpha)

def method_subplots_adjust(plot):
    
    plot.plt.subplots_adjust(
        top    = plot.top,
        bottom = plot.bottom,
        left   = plot.left,
        right  = plot.right,
        hspace = plot.hspace,
        wspace = plot.wspace)

def method_save(plot):
    if plot.filename:
        plot.plt.savefig(plot.filename, dpi=plot.dpi)

def method_show(plot):
    if plot.show is True:
        plot.plt.show()
    else:
        if plot.suppress is False:
            print('Ready for next subplot')
