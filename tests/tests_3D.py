import unittest
import numpy as np
from mpl_plotter.three_d import line, scatter, surface


class Tests(unittest.TestCase):

    def test_line(self):
        line(show=True, azim=33, elev=27,)

    def test_scatter(self):
        scatter(point_size=60,
                grid=True, grid_lines='-.',
                cmap='plasma', x_tick_number=5,
                color_bar=True, show=True,
                azim=33, elev=27,)

    def test_surface(self):
        surface(show=True, azim=155, elev=31,)
