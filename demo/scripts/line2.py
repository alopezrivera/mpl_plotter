import numpy as np
from mpl_plotter.two_d import line


def basic_line():
    """
    Quite basic line
    """

    line(show=True)


def medium_line():
    """
    Slightly customized line
    """

    line(show=True, pad_demo=True, spines_removed=None)


def custom_line():
    """
    Heavily customized line
    """

    line(norm=True, line_width=4,
         
         title="Custom Line", title_font="Pump Triline", title_size=40, title_color="orange",

         label_x="x", label_y="$\Psi$",
         label_size_x=30, label_size_y=20,
         label_pad_x=-0.05, label_pad_y=10,
         label_rotation_y=0,

         aspect=1,
         pad_demo=True,
         workspace_color="darkred",
         grid=True, grid_color="grey",
         
         tick_color="darkgrey", tick_label_decimals=4,
         tick_number_x=12, tick_number_y=12,
         tick_rotation_x=35,

         color_bar=True, cb_tick_number=5, cb_pad=0.05,

         show=True)


basic_line()
medium_line()
custom_line()
