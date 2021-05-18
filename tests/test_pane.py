import unittest
import numpy as np

import matplotlib.pyplot as plt
from mpl_plotter.presets.standard.publication import preset2
from mpl_plotter.presets.panes import Lines
from mpl_plotter.color.schemes import one


x = np.linspace(0, np.pi/4, 100000)
u = np.sin(x); uu = np.sinh(x)
v = np.cos(x); vv = np.cosh(x)
y = np.tan(x); yy = np.tanh(x)


from tests.setup import show


class Tests(unittest.TestCase):

    def test_n_pane_single(self):
        Lines(preset=preset2).n_pane_single(x,                   # Horizontal vector
                                            [u, v, y],           # List of curves to be plotted
                                            ["u", "v", "y"],     # List of vertical axis labels
                                            ["a", "b", "c"],     # List of legend labels
                                            show=show)
        if show:
            plt.show()

    def test_n_pane_comparison(self):
        Lines(preset=preset2).n_pane_comparison(x,                              # Horizontal vector
                                                [[u, uu], [v, vv], [y, yy]],    # List of pairs of curves to be compared
                                                ["u", "v", "y"],                # List of vertical axis labels
                                                ["a", "b"],                     # List of legend labels
                                                show=show)

        if show:
            plt.show()

    def test_lotapanes(self):
        print("GGGGGGGGGGGGGOIN")
        f = lambda n, x: np.sin(n**2*x)
        Lines(preset=preset2).n_pane_single(x,  # Horizontal vector
                                            [f(1, x),
                                             f(2, x),
                                             f(3, x),
                                             f(4, x),
                                             f(5, x),
                                             f(6, x),
                                             f(7, x),
                                             f(8, x),
                                             f(9, x),
                                             f(10, x),
                                             f(11, x),
                                             f(12, x)],  # List of curves to be plotted
                                            show=show)
        g = lambda n, x: np.cos(n*x)
        h = lambda n, x: np.cos((20-n)*x)
        Lines(preset=preset2).n_pane_comparison(x,  # Horizontal vector
                                                [[f(1,  x), g(1,  x), h(1,  x)],
                                                 [f(2,  x), g(2,  x), h(2,  x)],
                                                 [f(3,  x), g(3,  x), h(3,  x)],
                                                 [f(4,  x), g(4,  x), h(4,  x)],
                                                 [f(5,  x), g(5,  x), h(5,  x)],
                                                 [f(6,  x), g(6,  x), h(6,  x)],
                                                 [f(7,  x), g(7,  x), h(7,  x)],
                                                 [f(8,  x), g(8,  x), h(8,  x)],
                                                 [f(9,  x), g(9,  x), h(9,  x)],
                                                 [f(10, x), g(10, x), h(10, x)],
                                                 [f(11, x), g(11, x), h(11, x)],
                                                 [f(12, x), g(12, x), h(12, x)]],  # List of curves to be plotted
                                                zorders=[0, 2, 1],
                                                alphas=[0.5, 1, 0.75],
                                                colors=one()[5:8],
                                                show=show
                                                )
        if show:
            plt.show()
