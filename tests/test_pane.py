import unittest
import numpy as np

import matplotlib.pyplot as plt
from mpl_plotter.presets.standard.publication import preset
from mpl_plotter.presets.panes import Lines


x = np.linspace(0, np.pi/4, 100000)
u = np.sin(x); uu = np.sinh(x)
v = np.cos(x); vv = np.cosh(x)
y = np.tan(x); yy = np.tanh(x)


class Tests(unittest.TestCase):

    def test_n_pane_single(self):
        Lines(preset=preset).n_pane_single(x,                   # Horizontal vector
                                           [u, v, y],           # List of curves to be plotted
                                           ["u", "v", "y"],     # List of vertical axis labels
                                           ["a", "b", "c"]      # List of legend labels
                                           )
        plt.show()

    def test_n_pane_comparison(self):
        Lines(preset=preset).n_pane_comparison(x,                               # Horizontal vector
                                               [[u, uu], [v, vv], [y, yy]],     # List of pairs of curves to be compared
                                               ["u", "v", "y"],                 # List of vertical axis labels
                                               ["a", "b"]                       # List of legend labels
                                               )

        plt.show()

    def test_lotapanes(self):
        f = lambda n, x: np.sin(n**2*x)
        Lines(preset=preset).n_pane_single(x,  # Horizontal vector
                                           [f(1,  x),
                                            f(2,  x),
                                            f(3,  x),
                                            f(4,  x),
                                            f(5,  x),
                                            f(6,  x),
                                            f(7,  x),
                                            f(8,  x),
                                            f(9,  x),
                                            f(10, x),
                                            f(11, x),
                                            f(12, x)],  # List of curves to be plotted
                                           )
        plt.show()
