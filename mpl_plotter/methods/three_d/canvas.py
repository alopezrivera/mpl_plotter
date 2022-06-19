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
        if self.fig is None:
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                axes = self.fig.axes
                for ax in axes:
                    if ax.__class__.__name__ == 'Axes3DSubplot':
                        self.ax = ax

        if self.ax is None:
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box', projection='3d')

        self.ax.view_init(azim=self.azim, elev=self.elev)

    def method_workspace_style(self):
        if self.light:
            self.workspace_color = 'black' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = None

    def method_pane_fill(self):
        # Pane fill - False by default
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        # Pane color - transparent by default
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        if self.pane_fill is not None:
            # Set pane fill to True if a color is provided
            self.ax.xaxis.pane.fill = True if self.pane_fill is not None else False
            self.ax.yaxis.pane.fill = True if self.pane_fill is not None else False
            self.ax.zaxis.pane.fill = True if self.pane_fill is not None else False
            # Set pane fill color to that specified
            self.ax.xaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))
            self.ax.yaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))
            self.ax.zaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))

        # Set edge colors
        if self.blend_edges:
            if self.pane_fill is not None:
                spine_color = self.pane_fill
            else:
                spine_color = (0, 0, 0, 0)
        else:
            spine_color = self.spine_color

        self.ax.xaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "x")
                                         else self.background_color_plot)
        self.ax.yaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "y")
                                         else self.background_color_plot)
        self.ax.zaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "z")
                                         else self.background_color_plot)

    def method_background_color(self):
        self.fig.patch.set_facecolor(self.background_color_figure)
        self.ax.set_facecolor(self.background_color_plot)
        self.ax.patch.set_alpha(self.background_alpha)

    def method_spines(self):

        if self.spines_juggled is not None:
            self.ax.xaxis._axinfo['juggled'] = self.spines_juggled
        else:
            self.ax.xaxis._axinfo['juggled'] = (1, 0, 2)

    def method_remove_axes(self):
        if self.remove_axis is not None:
            for axis in np.array(self.remove_axis).flatten():
                if axis == "x":
                    self.ax.xaxis.line.set_lw(0.)
                    self.ax.set_xticks([])
                if axis == "y":
                    self.ax.yaxis.line.set_lw(0.)
                    self.ax.set_yticks([])
                if axis == "z":
                    self.ax.zaxis.line.set_lw(0.)
                    self.ax.set_zticks([])

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
        if self.show is True:
            self.plt.show()
        else:
            if self.suppress is False:
                print('Ready for next subplot')
