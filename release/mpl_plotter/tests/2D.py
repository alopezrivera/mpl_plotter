from two_d import heatmap, line, quiver, scatter, streamline


def i():
    heatmap(color_bar=True)


def j():
    line(grid=True, grid_lines='-.', x_tick_number=5, legend=True)


def k():
    quiver(x_bounds=[0, 1], y_bounds=[0, 1],
           custom_x_tick_labels=[100, 1000], custom_y_tick_labels=[9, -9])


def l():
    def t1():
        scatter(grid=True, grid_lines='-.', cmap='magma', x_tick_number=5, legend=True, color_bar=True)

    def t2():
        import numpy as np
        x = np.linspace(0, 10, 1000)
        y = np.sinh(x)
        scatter(x=x, y=y, c=x, color_bar=True, resize_axes=True, x_resize_pad=1, y_resize_pad=1000)

    t1()
    t2()


l()


def m():
    streamline()
