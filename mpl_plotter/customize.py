import inspect
from importlib import import_module

from mpl_plotter.two_d import canvas, attributes


class custom_canvas(canvas):

    def __init__(self,
                 # Base
                 backend=None,
                 # Fonts
                 font='serif', math_font="dejavusans", font_color="black",
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 style=None,
                 # Grid
                 grid=False, grid_color='lightgrey', grid_lines='-.',
                 ):

        """
        Custom canvas class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error:
                            - python configuration problem -> backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(custom_canvas).parameters:
            setattr(self, item, eval(item))

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        # Custom canvas
        self.method_backend()
        self.method_fonts()
        self.method_setup()
        self.method_grid()



class customize(canvas, attributes):

    def __init__(self,
                 # Base
                 backend=None,
                 # Fonts
                 font='serif', math_font="dejavusans", font_color="black",
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, prune=None, resize_axes=True, aspect=None,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=('top', 'right'),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=False, grid_color='lightgrey', grid_lines='-.',
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_locations=None, custom_y_tick_locations=None, fine_tick_locations=True,
                 custom_x_tick_labels=None, custom_y_tick_labels=None,
                 date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=True, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):

        """
        Customize plot class
        mpl_plotter - 2D
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(customize).parameters:
            setattr(self, item, eval(item))

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        # Canvas setup
        self.method_backend()
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_background_color()
        self.method_workspace_style()

        # Legend
        self.method_legend()

        # Resize axes
        # self.method_resize_axes()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        # self.method_ticks()
