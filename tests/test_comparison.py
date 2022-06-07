# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np

from mpl_plotter.two_d import comparison, line, scatter

from tests.setup import show, backend


x = np.linspace(0, np.pi/4, 50)
u = np.sin(x); uu = np.sinh(x)
v = np.cos(x); vv = np.cosh(x)
w = np.tan(x); yy = np.tanh(x)


class TestsInput(unittest.TestCase):

    def test_comparison_1(self):

        comparison(x,
                   u,
                   plot_labels=["sin", "cos", "tan"],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )

    def test_comparison_2(self):

        comparison([x],
                   [u],
                   plot_labels=["sin", "cos", "tan"],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )

    def test_comparison_3(self):

        comparison([x],
                   [u, v, w],
                   plot_labels=["sin", "cos", "tan"],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )

    def test_comparison_4(self):

        comparison([x, x, x],
                   [u, v, w],
                   plot_labels=["sin", "cos", "tan"],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )


class TestsPlotters(unittest.TestCase):
    def test_comparison_mix(self):
        comparison([x, x, x],
                   [u, v, w],
                   [line, scatter, scatter],
                   plot_labels=["sin", "cos", "tan"],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )

    def test_comparison_custom_f(self):

        def f(x, y, **kwargs):
            line(x, y,
                 line_width=2,
                 **kwargs)
        def g(x, y, **kwargs):
            scatter(x, y,
                    scatter_marker=2,
                    scatter_size=10,
                    **kwargs)
        def h(x, y, **kwargs):
            scatter(x, y,
                    scatter_marker="s",
                    scatter_size=5,
                    **kwargs)

        comparison([x, x, x],
                   [u, v, w],
                   [f, g, h],
                   plot_labels=["sin", "cos", "tan"],
                   zorders=[1, 2, 3],
                   colors=['C1', 'C2', 'C3'],
                   alphas=[0.5, 0.5, 1],
                   tick_labels_x=[0, r"$\frac{\pi}{8}$", r"$\frac{\pi}{4}$"],
                   show=show, backend=backend,
                   aspect=1
                   )
