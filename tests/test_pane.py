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
