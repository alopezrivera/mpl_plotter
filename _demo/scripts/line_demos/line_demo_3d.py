import numpy as np
from mpl_plotter.three_d import line


def basic_line():
    """
    Quite basic line
    """

    line(show=True,
         # Basic setup
         figsize=(7, 8), azim=33, elev=27,)


def medium_line():
    """
    Slightly customized line
    """

    line(show=True,
         # Basic setup
         figsize=(7, 8), azim=33, elev=27,
         # Some customization
         x_label=None, y_label=None, z_label=None,
         demo_pad_plot=True, color="green",
         x_tick_number=3, x_tick_label_size=10, x_custom_tick_locations=[-0.5, 0.5],
         y_tick_number=1, y_tick_label_size=20,
         z_tick_number=1, z_tick_label_size=20,
         )


def custom_line():
    """
    Heavily customized line
    """

    line(show=True,
         # Basic setup
         figsize=(7, 8), azim=33, elev=27,
         # Specifics
         line_width=10,
         # Color
         color="black",
         # Bounds
         demo_pad_plot=True,
         # Title
         title="Custom Line", title_font="Pump Triline", title_size=100, title_color="orange", title_y=0.95,
         # Labels
         x_label="x", x_label_size=30, x_label_pad=25,
         y_label="$\Psi$", y_label_size=30, y_label_rotation=0, y_label_pad=25,
         # Ticks
         tick_color="darkorange", tick_ndecimals=4,
         x_tick_number=12, y_tick_number=12,
         x_tick_rotation=-35, y_tick_rotation=25,
         # Color bar
         color_bar=True, cb_tick_number=5,
         # Scene colors
         workspace_color="darkred",
         pane_fill="#fff9de",
         # Grid
         grid=True, grid_color="grey"
         )


# basic_line()
# medium_line()
custom_line()
