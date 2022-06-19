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
