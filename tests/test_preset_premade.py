import unittest
import numpy as np

from mpl_plotter.color.schemes import one


x = np.linspace(0, 4, 1000)
y = np.exp(x)
z = abs(np.sin(x) * np.exp(x))


class Tests(unittest.TestCase):

    def test_publication(self):
        from mpl_plotter.presets.publication import two_d
        two_d.line(x, z, scale=1/20, color=one()[5], show=True)

    def test_precision(self):
        from mpl_plotter.presets.precision import two_d as two_d_precision
        two_d_precision.line(x, z, scale=1/20, color=one()[5], show=True)
