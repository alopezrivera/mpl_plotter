import unittest
import numpy as np
from mpl_plotter.two_d import line

from tests.setup import show, backend


class DemoTests(unittest.TestCase):

    def basic_line(self):
        """
        Quite basic line
        """

        line(show=show, backend=backend)


    def medium_line(self):
        """
        Slightly customized line
        """

        line(show=show, demo_pad_plot=True, spines_removed=None, backend=backend)


    def custom_line(self):
        """
        Heavily customized line
        """

        line(norm=True, line_width=4, backend=backend,
             aspect=1,
             show=show, demo_pad_plot=True,
             x_label="x", x_label_size=30, x_label_pad=-0.05,
             y_label="$\Psi$", y_label_size=30, y_label_rotation=0, y_label_pad=20,
             title="Custom Line", title_font="Pump Triline", title_size=40, title_color="orange",
             tick_color="darkgrey", workspace_color="darkred", tick_ndecimals=4,
             x_tick_number=12, y_tick_number=12,
             x_tick_rotation=35,
             color_bar=True, cb_tick_number=5, cb_pad=0.05,
             grid=True, grid_color="grey")
