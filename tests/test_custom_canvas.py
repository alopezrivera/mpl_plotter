# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np
import matplotlib.pyplot as plt
from mpl_plotter.canvas import custom_canvas2, custom_canvas3

from tests.setup import show, backend


x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x)
z = np.cos(x**2+y**2)


class Test(unittest.TestCase):

    def test2(self):
        c = custom_canvas2(x=x, y=y, spines_removed=None, font_color="darkred", backend=backend,
                           x_tick_number=1, x_tick_ndecimals=10, title="TITLE", y_label="sin")
        ax, fig = c.ax, c.fig

        plt.plot(x, y)

        if show:
            plt.show()

    def test2_wo_variables(self):
        # If x and y are not provided, axes and ticks (including font parameters) will not be modified
        c = custom_canvas2(spines_removed=None, font_color="darkred", backend=backend,
                           x_tick_number=1, x_tick_ndecimals=10,
                           title="TITLE", y_label="sin")
        ax, fig = c.ax, c.fig

        plt.plot(x, y)

        if show:
            plt.show()

    def test3(self):
        c = custom_canvas3(x=x, y=y, z=z, font_color="darkred", backend=backend,
                           x_tick_number=1,
                           y_tick_number=1,
                           z_tick_number=1,
                           grid=True,
                           pane_fill="#f7f7f7",
                           aspect_equal=True
                           )
        ax, fig = c.ax, c.fig

        ax.plot(x, y, z, linewidth=2, color="darkblue")
        ax.scatter(x, y, z, color="orange", s=1)

        if show:
            plt.show()
