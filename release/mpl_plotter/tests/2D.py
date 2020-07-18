def test_heatmap():
    from mpl_plotter.two_d import heatmap
    heatmap(color_bar=True)


def test_line():
    from mpl_plotter.two_d import line
    line(grid=True, grid_lines='-.', x_tick_number=5, legend=True)


def test_quiver():
    from mpl_plotter.two_d import quiver
    quiver(x_bounds=[0, 1], y_bounds=[0, 1])


def test_scatter():
    from mpl_plotter.two_d import scatter
    def t1():
        scatter(grid=True, grid_lines='-.', cmap='magma', x_tick_number=5, legend=True, color_bar=True)

    def t2():
        import numpy as np
        x = np.linspace(0, 10, 1000)
        y = np.sinh(x)
        scatter(x=x, y=y, c=x, color_bar=True, resize_axes=True, x_resize_pad=1, y_resize_pad=1000)

    t1()
    t2()


def test_streamline():
    from mpl_plotter.two_d import streamline
    streamline()
