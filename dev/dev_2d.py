import numpy as np
from mpl_plotter.two_d import fill_area, line, scatter


def fill():
    x = np.arange(-6, 6, .01)
    y = np.sin(x)
    z = np.sin(x-45/180*np.pi)

    line(x=x, y=y)
    line(x=x, y=z)
    fill_area(x=x, y=y, z=z,
              between=True, show=True, demo_pad_plot=True,
              font_color="darkred"
              )


def scattr():
    scatter(grid=True, grid_lines='-.', cmap='magma', x_tick_number=5,
            plot_label="Graph", legend=True,
            color_bar=True, show=True)


fill()
