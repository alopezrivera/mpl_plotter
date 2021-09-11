# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
MPL Plotter canvas methods
--------------------------
"""


import inspect
import matplotlib as mpl
from importlib import import_module

from mpl_plotter.two_d import canvas, attributes
from mpl_plotter.three_d import canvas as canvas3, attributes as attributes3


class custom_canvas2(canvas, attributes):

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
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
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
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
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
        for item in inspect.signature(custom_canvas2).parameters:
            setattr(self, item, eval(item))

        # Avoid issues resizing axes
        if isinstance(self.x, type(None)) or isinstance(self.y, type(None)):
            self.resize_axes = False
            self.modify_ticks = False
        else:
            self.resize_axes = True
            self.modify_ticks = True

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        # Canvas setup
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
        if self.modify_ticks:
            self.method_ticks()

    def _blank_preset(self):
        preset = "preset = {\n"
        for item in inspect.signature(custom_canvas2).parameters:
            if item not in ["x", "y"]:
                v = getattr(self, item) if item not in ["fig", "ax"] else None
                v_str = '"'+v+'"' if isinstance(v, str) else str(v)

                r_p = '    #"' + item + '": ' + v_str + ",\n"
                preset = preset + r_p

        preset = preset + "}"

        return preset


class custom_canvas3(canvas3, attributes3):

    def __init__(self,
                 # Placeholders
                 x=None, y=None, z=None,
                 # Scale
                 x_scale=1,
                 y_scale=1,
                 z_scale=1,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111, azim=-137, elev=26, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect=1, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 z_upper_bound=None, z_lower_bound=None,
                 x_bounds=None, y_bounds=None, z_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 z_upper_resize_pad=0, z_lower_resize_pad=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_weight='normal', x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_weight='normal', y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_weight='normal', z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None, x_custom_tick_labels=None, x_custom_tick_locations=None,
                 y_tick_number=5, y_tick_labels=None, y_custom_tick_labels=None, y_custom_tick_locations=None,
                 z_tick_number=5, z_tick_labels=None, z_custom_tick_labels=None, z_custom_tick_locations=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None,
                 x_tick_label_pad=4,
                 y_tick_label_pad=4,
                 z_tick_label_pad=4,
                 x_tick_ndecimals=1,
                 y_tick_ndecimals=1,
                 z_tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None, z_tick_label_size=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, newplot=False,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Custom canvas class
        mpl_plotter - 3D
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
        for item in inspect.signature(custom_canvas3).parameters:
            setattr(self, item, eval(item))

        # Avoid issues resizing axes
        if isinstance(self.x, type(None)) or isinstance(self.y, type(None)) or isinstance(self.z, type(None)):
            self.resize_axes = False
            self.modify_ticks = False
        else:
            self.resize_axes = True
            self.modify_ticks = True

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        # Canvas setup
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_pane_fill()
        self.method_background_color()
        self.method_workspace_style()
        # Scale axes
        self.method_scale()

        # Legend
        self.method_legend()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        if self.modify_ticks:
            self.method_ticks()
        self.method_remove_axes()

    def _blank_preset(self):
        preset = "preset = {\n"
        for item in inspect.signature(custom_canvas3).parameters:
            if item not in ["x", "y", "z"]:
                v = getattr(self, item) if item not in ["fig", "ax"] else None
                v_str = '"'+v+'"' if isinstance(v, str) else str(v)

                r_p = '    #"' + item + '": ' + v_str + ",\n"
                preset = preset + r_p

        preset = preset + "}"

        return preset


if __name__ == "__main__":
    print(custom_canvas2()._blank_preset())
    print("==========================")
    mpl.pyplot.show()
    print("==========================")
    print(custom_canvas3()._blank_preset())

