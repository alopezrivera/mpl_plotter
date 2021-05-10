import numpy as np
from mpl_plotter.three_d import line


def basic_line():
    """
    Quite basic line
    """

    line(show=True, figsize=(7, 8))


def medium_line():
    """
    Slightly customized line
    """

    line(show=True, demo_pad_plot=True, spines_juggled=(0, 1, 2),
         azim=33, elev=27,
         figsize=(7, 8),
         )


def custom_line():
    """
    Heavily customized line
    """

    line(line_width=4,
         figsize=(7, 8),
         aspect=1, azim=33, elev=27,
         show=True, demo_pad_plot=True,
         x_label="x", x_label_size=30, x_label_pad=25,
         y_label="$\Psi$", y_label_size=30, y_label_rotation=0, y_label_pad=25,
         title="Custom Line", title_font="Pump Triline", title_size=40, title_color="orange",
         tick_color="darkorange", workspace_color="darkred", tick_ndecimals=4,
         x_tick_number=12, y_tick_number=12,
         x_tick_rotation=-35, y_tick_rotation=25,
         color_bar=True, cb_tick_number=5,
         grid=True, grid_color="grey")


basic_line()
medium_line()
custom_line()
