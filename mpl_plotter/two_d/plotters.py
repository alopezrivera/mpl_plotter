# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Plotting Methods
----------------
"""

import re
import inspect
import warnings
import numpy as np
import pandas as pd
import datetime as dt
from importlib import import_module

import matplotlib as mpl
from matplotlib import cm

# METHODS
from mpl_plotter.two_d.components import canvas
from mpl_plotter.two_d.components import guides
from mpl_plotter.two_d.components import framing
from mpl_plotter.two_d.components import text

from mpl_plotter.two_d.mock import MockData

from mpl_plotter.utils import ensure_ndarray


# Override NumPy ufunc size changed warning (https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility)
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


class plot(canvas, guides, framing, text):

    def init(self):

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        """
        Run
        """

        self.run()

    def run(self):
        self.main()
        self.finish()

    def main(self):
        # Canvas setup
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_background_color()
        self.method_workspace_style()

        # Mock plot
        self.mock()
        # Plot
        self.plot()

    def finish(self):
        # Resize axes
        self.method_resize_axes()
        # Legend
        self.method_legend()
        # Colorbar
        self.method_colorbar()

        # Text
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_tick_locs()
        self.method_tick_labels()

        # Adjust
        self.method_subplots_adjust()

        # Save
        self.method_save()

        self.method_show()


class line(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, line_width=2,
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Line plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param line_width: Line width

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
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
        for item in inspect.signature(line).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None

        self.init()

    def plot(self):

        if self.color_rule is None:
            self.graph = self.ax.plot(self.x, self.y, label=self.plot_label, linewidth=self.line_width,
                                      color=self.color,
                                      zorder=self.zorder,
                                      alpha=self.alpha,
                                      )[0]
        else:
            # Create a set of line segments so that we can color them individually
            # This creates the points as a N x 1 x 2 array so that we can stack points
            # together easily to get the segments. The segments array for line collection
            # needs to be (numlines) x (points per line) x 2 (for x and y)
            points = np.array([self.x, self.y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            # Create a continuous norm to map from data points to colors
            color_range = self.color_rule(self.x) if hasattr(self.color_rule, '__call__') else self.color_rule
            norm        = self.plt.Normalize(color_range.min(), color_range.max())
            lc          = mpl.collections.LineCollection(segments, cmap=self.cmap, norm=norm)
            
            # Set the values used for colormapping
            lc.set_array(self.color_rule)
            lc.set_linewidth(self.line_width)
            self.graph = self.ax.add_collection(lc)
        
    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()
            if self.color_rule:
                self.color_rule = self.y


class scatter(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, scatter_size=5, scatter_marker='o', scatter_facecolors=None,
                 # Specifics: color
                 color="C0", cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Scatter plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param scatter_size: Point size
        :param scatter_marker: Dot scatter_marker

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
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
        for item in inspect.signature(scatter).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None

        self.init()

    def plot(self):
        
        self.graph = self.ax.scatter(self.x, self.y, label=self.plot_label,
                                     s=self.scatter_size, marker=self.scatter_marker, facecolors=self.scatter_facecolors,
                                     c=self.color_rule, cmap=self.cmap if self.color_rule is not None else None,
                                     zorder=self.zorder,
                                     alpha=self.alpha)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y  = MockData().spirograph()
            self.color_rule = self.y


class heatmap(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, heatmap_normvariant='SymLog',
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,                 
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Heatmap plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param heatmap_normvariant: Detailed information in the Matplotlib documentation

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """
        # T
        # urn all instance arguments to instance attributes
        for item in inspect.signature(heatmap).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.z = ensure_ndarray(self.z) if self.z is not None else None

        self.init()

    def plot(self):
        self.graph = self.ax.pcolormesh(self.x, self.y, self.z, cmap=self.cmap,
                                        zorder=self.zorder,
                                        alpha=self.alpha,
                                        label=self.plot_label,
                                        shading='auto'
                                        )
        # Resize axes
        self.method_resize_axes()

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y, self.z = MockData().waterdrop()
            self.color_rule = self.z


class quiver(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None,
                 quiver_rule=None, quiver_custom_rule=None,
                 quiver_vector_width=0.01, quiver_vector_min_shaft=2, quiver_vector_length_threshold=0.1,
                 # Color
                 color=None, cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,                 
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Quiver plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param u: u
        :param v: v
        :param quiver_rule: lambda function of u and v
            rule = lambda u, v: (u**2+v**2)
        :param quiver_custom_rule: Array assigning a color to each (x, y, u, v) vector
        :param quiver_vector_width: Vector width
        :param quiver_vector_min_shaft: Minimum vector shaft
        :param quiver_vector_length_threshold: Minimum vector length

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """
        # T
        # urn all instance arguments to instance attributes
        for item in inspect.signature(quiver).parameters:
            setattr(self, item, eval(item))


        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.init()

    def plot(self):

        # Color rule
        self.method_rule()

        self.graph = self.ax.quiver(self.x, self.y, self.u, self.v,
                                    color=self.color, cmap=self.cmap,
                                    width=self.quiver_vector_width,
                                    minshaft=self.quiver_vector_min_shaft,
                                    minlength=self.quiver_vector_length_threshold,
                                    label=self.plot_label,
                                    zorder=self.zorder,
                                    alpha=self.alpha
                                    )

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.random.random(100)
            self.y = np.random.random(100)
            self.u = np.random.random(100)
            self.v = np.random.random(100)
            self.color_rule = np.sqrt(self.u ** 2 + self.v ** 2)

    def method_rule(self):
        # Rule
        if isinstance(self.quiver_custom_rule, type(None)):
            if isinstance(self.quiver_rule, type(None)):
                self.quiver_rule = lambda u, v: (u ** 2 + v ** 2)
            self.quiver_rule = self.quiver_rule(u=self.u, v=self.v)
        else:
            self.quiver_rule = self.quiver_custom_rule

        # Color determined by rule function
        c = self.quiver_rule
        # Flatten and normalize
        c = (c.ravel() - c.min())/c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(self.cmap)
        self.color = cmap(c)


class streamline(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None, streamline_line_width=1, streamline_line_density=2,
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,                 
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Streamline class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param u: u
        :param v: v
        :param line_width: Streamline width
        :param streamline_density: Measure of the amount of streamlines displayed. Low value (default=2)


        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
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
        for item in inspect.signature(streamline).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.u = ensure_ndarray(self.u) if self.u is not None else None
        self.v = ensure_ndarray(self.v) if self.v is not None else None

        self.init()

    def plot(self):

        # Color rule
        self.method_rule()

        # Plot
        self.graph = self.ax.streamplot(self.x, self.y, self.u, self.v,
                                        color=self.color,
                                        cmap=self.cmap,
                                        linewidth=self.streamline_line_width,
                                        density=self.streamline_line_density,
                                        zorder=self.zorder,
                                        ).lines

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.linspace(0, 10, 100)
            self.y = np.linspace(0, 10, 100)
            self.x, self.y = np.meshgrid(self.x, self.y)
            self.u = np.cos(self.x)
            self.v = np.cos(self.y)
            self.color = self.color_rule = self.u

    def method_rule(self):
        if isinstance(self.color, type(None)):
            rule_color = lambda u: np.sqrt(self.u ** 2 + self.v ** 2) / np.sqrt(self.u.max() ** 2 + self.v.max() ** 2)
            self.color = rule_color(self.u)


class fill_area(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, fill_area_between=False, fill_area_below=False, fill_area_above=False,
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, color_rule=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bounds_x=None, bounds_y=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=17, title_pad=20, title_weight=None, title_font='Latin Modern Roman', title_color=None,
                 # Labels
                 label_x=None, label_size_x=12, label_pad_x=10, label_rotation_x=None, label_weight_x=None,
                 label_y=None, label_size_y=12, label_pad_y=10, label_rotation_y=None, label_weight_y=None,
                 # Ticks
                 tick_number_x=5,
                 tick_number_y=5,
                 label_coords_x=None, label_coords_y=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, tick_label_size_x=None, tick_label_size_y=None,
                 tick_bounds_fit=True,
                 tick_locations_x=None, tick_bounds_x=None,                 
                 tick_locations_y=None, tick_bounds_y=None,
                 tick_labels_x=None, tick_labels_y=None,
                 tick_labels_dates_x=False, date_format='%Y-%m-%d',
                 tick_label_decimals=1, tick_label_decimals_x=None, tick_label_decimals_y=None,
                 tick_rotation_x=None, tick_rotation_y=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 colorbar=False, cb_orientation='vertical', cb_shrink=1.0,
                 cb_floating=False, cb_floating_coords=[0.905, 0.165], cb_floating_dimensions=[0.01, 0.8],
                 cb_anchored_pad=0.2,
                 cb_norm=None, cb_tick_locs=None, cb_tick_number=5, cb_vmin=None, cb_vmax=None,
                 cb_title=None, cb_title_size=10, cb_title_rotation=0,
                 cb_title_font=None, cb_title_style='normal', cb_title_weight='normal',
                 cb_title_top_loc=None, cb_title_top_pad=None,
                 cb_title_floating=False, cb_title_floating_coords=[0.0, 1.0], cb_title_floating_transform='transAxes',
                 cb_title_anchored_side=False, cb_title_anchored_pad=0.2,
                 cb_tick_label_decimals=1, cb_tick_label_size=10, cb_tick_label_pad=5,
                 cb_hard_bounds=False, cb_extend='neither',
                 cb_outline_width=None, cb_outline_color=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 top=0.930,
                 bottom=0.105,
                 left=0.165,
                 right=0.87,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Fill area class
        mpl_plotter - 2D

        Specifics
        :param x: Horizontal axis values
        :param y: Curve 1
        :param z: Curve 2

        The following parameters can be used in combination:

        :param between: Fill between Curve 1 and Curve 2
        :param below: Fill below Curve 1 and Curve 2
        :param above: Fill above Curve 1 and Curve 2

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

        Other
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
        for item in inspect.signature(fill_area).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.z = ensure_ndarray(self.z) if self.z is not None else None

        self.init()

    def plot(self):

        """
        Fill the region below the intersection of S and Z
        """
        if self.z is not None:
            if self.fill_area_between:
                self.ax.fill_between(self.x, self.y, self.z, facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if self.fill_area_below:
                self.ax.fill_between(self.x, self.i_below(), np.zeros(self.y.shape), facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if self.fill_area_above:
                self.ax.fill_between(self.x, self.i_above(), np.zeros(self.y.shape), facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if not self.fill_area_between and not self.fill_area_below and not self.fill_area_above:
                print_color('No area chosen to fill: specify whether to fill "between", "below" or "above" the curves',
                            'grey')
        else:
            self.ax.fill_between(self.x, self.y, np.zeros(self.y.shape), facecolor=self.color, alpha=self.alpha)

    def i_below(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] <= self.z[i] else self.z[i]
        return c

    def i_above(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] >= self.z[i] else self.z[i]
        return c

    def intersection(self):
        return np.nonzero(np.absolute(self.y - self.z) == min(np.absolute(self.y - self.z)))[0]

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.arange(-6, 6, .01)
            self.y = MockData().boltzman(self.x, 0, 1)
            self.z = 1 - MockData().boltzman(self.x, 0.5, 1)
            line(x=self.x, y=self.y,
                 grid=False, resize_axes=False,
                 ax=self.ax, fig=self.fig)
            line(x=self.x, y=self.z,
                 grid=False, resize_axes=False,
                 ax=self.ax, fig=self.fig)
            self.fill_area_below = True
