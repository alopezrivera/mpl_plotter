import numpy as np
from mpl_plotter.three_d import line


def basic_line():
    """
    Quite basic line
    """

    line(show=True,
         # Basic setup
         figsize=(7, 8), azim=33, elev=27)


def medium_line():
    """
    Slightly customized line
    """

    line(show=True,
         # Basic setup
         figsize=(7, 8), azim=33, elev=27,
         # Some customization
         label_x=None, label_y=None, label_z=None,
         pad_demo=True, color="green",
         tick_number_x=3, tick_label_size_x=10, tick_locations_x=[-0.5, 0.5],
         tick_number_y=1, tick_label_size_y=20,
         tick_number_z=1, tick_label_size_z=20)


def custom_line():
    """
    Heavily customized line
    """

    line(figsize=(7, 8), azim=33, elev=27,
         # Specifics
         line_width=10,
         # Color
         color="black",
         # Bounds
         pad_demo=True,
         # Title
         title="Custom Line", title_font="Pump Triline", title_size=80, title_color="orange", title_y=0.95,
         # Labels
         label_x="x", label_size_x=30, label_pad_x=25,
         label_y="$\Psi$", label_size_y=30, label_rotation_y=0, label_pad_y=25,
         # Ticks
         tick_color="darkorange",
         tick_label_decimals=4,
         tick_number_x=12, tick_number_y=12,
         tick_rotation_x=-35, tick_rotation_y=25,
         # Scene colors
         workspace_color="darkred",
         pane_fill="#fff9de",
         # Grid
         grid=True, grid_color="grey",

         show=True)


# basic_line()
# medium_line()
custom_line()
