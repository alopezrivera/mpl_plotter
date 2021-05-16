import inspect
import matplotlib as mpl
from importlib import import_module

from mpl_plotter.two_d import canvas, attributes


def figure(figsize=(6, 6), backend='Qt5Agg'):
    if not isinstance(backend, type(None)):
        mpl.use(backend)
    import matplotlib.pyplot as plt
    return plt.figure(figsize=figsize)


class custom_canvas(canvas, attributes):

    def __init__(self,
                 # Placeholders
                 x=None, y=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, prune=None, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=None, norm=None,
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, tick_ndecimals_cb=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
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
        self.method_resize_axes()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
