import unittest
import numpy as np
from mpl_plotter.two_d import heatmap, line, quiver, scatter, streamline


class Tests(unittest.TestCase):

    def test_line(self):
        x = np.linspace(0, 10, 1000)
        y = np.sinh(x)
        line(x=x, y=y, norm=y,
             grid=True, grid_lines='-.', x_tick_number=5, color_bar=True)

    def test_scatter(self):
        def t1():
            scatter(grid=True, grid_lines='-.', cmap='magma', x_tick_number=5,
                    plot_label="Graph", legend=True,
                    color_bar=True)

        def t2():
            x = np.linspace(0, 10, 1000)
            y = np.sinh(x)
            scatter(x=x, y=y, norm=y, color_bar=True, resize_axes=True)

        import matplotlib.pyplot as plt
        t1()
        plt.clf()
        t2()

    def test_heatmap(self):
        heatmap(color_bar=True)

    def test_quiver(self):
        quiver(x_bounds=[0, 1], y_bounds=[0, 1],
               custom_x_tick_labels=[100, 1000], custom_y_tick_labels=[9, -9],
               color_bar=True)

    def test_streamline(self):
        x = np.linspace(0, 10, 1000)
        y = np.linspace(0, 10, 1000)
        x, y = np.meshgrid(x, y)
        u = np.cos(x)
        v = np.cos(y)
        streamline(x=x, y=y, u=u, v=v, color=u, color_bar=True)

    def test_fill(self):
        from mpl_plotter.two_d import fill_area
        fill_area()
