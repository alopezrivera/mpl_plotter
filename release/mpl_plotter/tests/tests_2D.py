import numpy as np
from two_d import heatmap, line, quiver, scatter, streamline


def test_line():
    x = np.linspace(0, 10, 1000)
    y = np.sinh(x)
    line(x=x, y=y, norm=y,
         grid=True, grid_lines='-.', x_tick_number=5, color_bar=True)


def test_scatter():
    def t1():
        scatter(grid=True, grid_lines='-.', cmap='magma', x_tick_number=5, legend=True, color_bar=True)

    def t2():
        x = np.linspace(0, 10, 1000)
        y = np.sinh(x)
        scatter(x=x, y=y, color_bar=True, resize_axes=True)

    t1()
    t2()


def test_heatmap():
    heatmap(color_bar=True)


def test_quiver():
    quiver(x_bounds=[0, 1], y_bounds=[0, 1],
           custom_x_tick_labels=[100, 1000], custom_y_tick_labels=[9, -9],
           color_bar=True)


def test_streamline():
    x = np.linspace(0, 10, 1000)
    y = np.linspace(0, 10, 1000)
    x, y = np.meshgrid(x, y)
    u = np.cos(x)
    v = np.cos(y)
    streamline(x=x, y=y, u=u, v=v, color=u, color_bar=True)


def test_fill():
    from two_d import fill_area
    fill_area()
