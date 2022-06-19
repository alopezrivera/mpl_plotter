# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Canvas
------
"""

import numpy as np
import matplotlib as mpl

from mpl_plotter import figure


class canvas:

    def method_backend(self):
        if self.backend is not None:
            try:
                mpl.use(self.backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(self.backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

    def method_figure(self):
        if self.style is not None:
            self.plt.style.use(self.style)
        self.fig = figure(figsize=self.figsize)

    def method_setup(self):
        if isinstance(self.fig, type(None)):
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                self.ax = self.plt.gca()

        if isinstance(self.ax, type(None)):
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_workspace_style(self):
        if self.light:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193/256, 193/256, 193/256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89/256, 89/256, 89/256) if isinstance(self.workspace_color2,
                                                                                 type(
                                                                                     None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193/256, 193/256, 193/256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2

    def method_background_color(self):
        self.fig.patch.set_facecolor(self.background_color_figure)
        self.ax.set_facecolor(self.background_color_plot)
        self.ax.patch.set_alpha(self.background_alpha)

    def method_spines(self):
        for spine in self.ax.spines.values():
            spine.set_color(self.workspace_color if isinstance(self.spine_color, type(None)) else self.spine_color)

        if self.spines_removed is not None:
            for i in range(len(self.spines_removed)):
                if self.spines_removed[i] == 1:
                    self.ax.spines[["left", "bottom", "top", "right"][i]].set_visible(False)

        # Axis ticks
        left, bottom, top, right = self.ticks_where
        # Tick labels
        labelleft, labelbottom, labeltop, labelright = self.tick_labels_where

        self.ax.tick_params(axis='both', which='both',
                            top=top, right=right, left=left, bottom=bottom,
                            labeltop=labeltop, labelright=labelright, labelleft=labelleft, labelbottom=labelbottom)

    def method_subplots_adjust(self):
        
        self.plt.subplots_adjust(
            top    = self.top,
            bottom = self.bottom,
            left   = self.left,
            right  = self.right,
            hspace = self.hspace,
            wspace = self.wspace)

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.show:
            # self.fig.tight_layout()
            self.plt.show()
        else:
            if not self.suppress:
                print('Ready for next subplot')

