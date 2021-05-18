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

        # Input
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x)
        line(x=x, y=y, show=show, backend=backend, aspect=1)

    def test_three_d(self):
        from mpl_plotter.three_d import line, scatter, surface

        line(show=show, backend=backend)

        scatter(show=show, backend=backend)

        surface(show=show, backend=backend)

        # Wireframe
        surface(show=show, backend=backend, alpha=0, line_width=0.5, edge_color="red", cstride=12, rstride=12)
