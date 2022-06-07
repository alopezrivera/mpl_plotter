# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np


from tests.setup import show, backend


class TestAll(unittest.TestCase):

    def test_two_d(self):
        from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area

        line(show=show, backend=backend)

        scatter(show=show, backend=backend)

        heatmap(show=show, backend=backend)

        quiver(show=show, backend=backend)

        streamline(show=show, backend=backend)

        fill_area(show=show, backend=backend)

    def test_three_d(self):
        from mpl_plotter.three_d import line, scatter, surface

        line(show=show, backend=backend)

        scatter(show=show, backend=backend)

        surface(show=show, backend=backend)

        # Wireframe
        surface(show=show, backend=backend, 
                surface_alpha=0,
                surface_wire_width=0.5,
                surface_edge_color="red",
                surface_cstride=12,
                surface_rstride=12)
