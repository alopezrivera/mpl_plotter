import unittest
import numpy as np

from mpl_plotter.presets.publication import two_d
from mpl_plotter.presets.precision import two_d as two_d_precision

from mpl_plotter.color.schemes import one


x = np.linspace(0, 4, 1000)
y = np.exp(x)
z = abs(np.sin(x) * np.exp(x))


class Tests(unittest.TestCase):

    def test_publication(self):

        two_d.line(x, z, aspect=0.05, color=one()[-2], show=True)

    def test_precision(self):

        two_d_precision.line(x, z, aspect=0.05, color=one()[-2], show=True)
