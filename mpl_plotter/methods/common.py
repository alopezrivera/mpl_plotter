# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Common
------
"""

import numpy as np

import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter import figure, get_available_fonts

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

def method_colorbar(plot):

    if plot.colorbar:

        assert plot.color_rule is not None or plot.cb_norm is not None, "You must specify a **color_rule** or **cb_norm** to display a colorbar."

        if plot.cb_vmin is None:
            plot.cb_vmin = plot.cb_norm.vmin if plot.cb_norm is not None else plot.color_rule.min()
        if plot.cb_vmax is None:
            plot.cb_vmax = plot.cb_norm.vmax if plot.cb_norm is not None else plot.color_rule.max()

        plot.graph.set_clim([plot.cb_vmin, plot.cb_vmax])
            
        plot.cb_tick_locs = plot.cb_tick_locs if plot.cb_tick_locs is not None else np.linspace(plot.cb_vmin,
                                                                                                plot.cb_vmax,
                                                                                                plot.cb_tick_number)
        
        plot.cb_norm = plot.cb_norm = plot.cb_norm if plot.cb_norm is not None else mpl.colors.Normalize(vmin=plot.cb_vmin,
                                                                                                         vmax=plot.cb_vmax)
        cb_mappable  = mpl.cm.ScalarMappable(norm=plot.cb_norm, cmap=plot.cmap)
        
        if plot.cb_floating:

            plot.cb_ax   = plot.fig.add_axes([*plot.cb_floating_coords, *plot.cb_floating_dimensions])
            
            cb = plot.plt.colorbar(mappable    = cb_mappable,
                                   cax         = plot.cb_ax,
                                   orientation = plot.cb_orientation,
                                   shrink      = plot.cb_shrink,
                                   ticks       = plot.cb_tick_locs,
                                   extend      = plot.cb_extend,
                                   boundaries  = plot.cb_tick_locs if plot.cb_hard_bounds else None)
            
        else:
            
            cb = plot.fig.colorbar(mappable    = cb_mappable,
                                   ax          = plot.ax,
                                   orientation = plot.cb_orientation,
                                   shrink      = plot.cb_shrink,
                                   ticks       = plot.cb_tick_locs,
                                   extend      = plot.cb_extend,
                                   boundaries  = plot.cb_tick_locs if plot.cb_hard_bounds else None,
                                   spacing     = 'proportional',
                                   format      = f'%.{plot.cb_tick_label_decimals}f',
                                   pad         = plot.cb_anchored_pad)
            plot.cb_ax = cb.ax
        
        # Title
        if plot.cb_title_floating:
            title = plot.cb_ax.text(x          = plot.cb_title_floating_coords[0],
                                    y          = plot.cb_title_floating_coords[1],
                                    s          = plot.cb_title,
                                    fontsize   = plot.cb_title_size,
                                    rotation   = plot.cb_title_rotation, 
                                    transform  = getattr(plot.cb_ax, plot.cb_title_floating_transform))
        else:
            title = plot.cb_ax.set_title(label    = plot.cb_title,
                                         pad      = plot.cb_title_anchored_pad,
                                         fontsize = plot.cb_title_size,
                                         fontdict = {'verticalalignment':   'baseline',
                                                     'horizontalalignment': 'center'},
                                         rotation = plot.cb_title_rotation)
            
        title_font = mpl.font_manager.FontProperties(family=plot.cb_title_font if plot.cb_title_font is not None else plot.font_typeface,
                                                     style=plot.cb_title_style,
                                                     size=plot.cb_title_size + plot.font_size_increase,
                                                     weight=plot.cb_title_weight)
        title.set_font_properties(title_font)

        # Ticks
        tick_axis = 'x' if plot.cb_orientation == 'horizontal' else 'y'
        cb.ax.tick_params(axis=tick_axis, direction='out')

        # plot.cb_ax.yaxis.set_major_formatter(FormatStrFormatter(f'%.{plot.cb_tick_label_decimals}f'))
        getattr(cb.ax, f'{tick_axis}axis').set_major_formatter(FormatStrFormatter(f'%.{plot.cb_tick_label_decimals}f'))
        getattr(cb.ax, f'{tick_axis}axis').set_tick_params(pad=plot.cb_tick_label_pad, labelsize=plot.cb_tick_label_size)
        
        
        # Outline
        cb.outline.set_edgecolor(plot.cb_outline_color if plot.cb_outline_color is not None else plot.workspace_color)
        cb.outline.set_linewidth(plot.cb_outline_width)
        
        # Make plot axis active again
        plot.plt.sca(plot.ax)

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
    
    # Shape
    assert plot.font_family in ['serif', 'cursive', 'sans-serif', 'monospace', 'fantasy'], f'The provided font shape "{plot.font_family}" is not supported. Supported font shapes are:\n   - "serif"\n   - "cursive"\n   -"sans-serif"\n   -"monospace"\n   -"fantasy"'
    mpl.rcParams['font.family'] = plot.font_family
    
    # Typeface
    if plot.font_typeface is not None:
        mpl.rcParams['font.family'] = 'serif'
        typeface = mpl.rcParams['font.serif'].insert(0, plot.font_typeface)
    else:
        plot.font_typeface = mpl.rcParams[f'font.{plot.font_family}'][0]

    assert plot.font_typeface in get_available_fonts(True), f'The chosen typeface "{plot.font_typeface}" is not available in your system. You can either install the font on your system, or choose one of the fonts installed in your system (use mpl_plotter.get_available_fonts to list them all).'
        
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
