# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Plotting Methods
----------------
"""

import inspect
import difflib
import warnings
import numpy as np
import matplotlib as mpl

from matplotlib import cm
from matplotlib.colors import LightSource

from importlib import import_module

# METHODS
from mpl_plotter.three_d.components import canvas
from mpl_plotter.three_d.components import guides
from mpl_plotter.three_d.components import framing
from mpl_plotter.three_d.components import text

from mpl_plotter.three_d.mock import MockData

from mpl_plotter.utils import ensure_ndarray


class plot(canvas, guides, framing, text):

    def init(self):

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        self.main()
        self.finish()

    def main(self):
        # Canvas setup
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_pane_fill()
        self.method_background_color()
        self.method_workspace_style()

        # Mock plot
        self.mock()
        # Plot
        self.plot()

    def finish(self):
        # Scale and axis resizing
        self.method_resize_axes()
        self.method_scale()

        # Legend
        self.method_legend()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_tick_locs()
        self.method_tick_labels()
        self.method_remove_axes()

        # Adjust
        self.method_subplots_adjust()

        # Save
        self.method_save()

        self.method_show()


class line(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, line_width=5, line_alpha=1,
                 # Specifics: color
                 color='darkred', cmap='RdBu_r',
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font='Latin Modern Roman',
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_bounds_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_bounds_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_bounds_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Line class
        mpl_plotter - 3D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param line_width: Line width

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        "param surface_norm: Norm to assign colormap values

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

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):

        self.graph = self.ax.plot3D(self.x, self.y, self.z, alpha=self.line_alpha, linewidth=self.line_width,
                                    color=self.color, label=self.plot_label)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 1000)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)


class scatter(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, scatter_size=30, scatter_marker="o", 
                 scatter_facecolors=None, color_rule=None, scatter_alpha=1,
                 # Color
                 color='darkred', cmap='RdBu_r',
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
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font='Latin Modern Roman',
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_bounds_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_bounds_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_bounds_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Scatter class
        mpl_plotter - 3D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param scatter_size: Point size
        :param scatter_marker: Dot scatter_marker

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        "param surface_norm: Norm to assign colormap values

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

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):

        if self.color_rule is not None:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.scatter_size, marker=self.scatter_marker, facecolors=self.scatter_facecolors,
                                         c=self.color_rule, cmap=self.cmap,
                                         alpha=self.scatter_alpha)
            self.method_colorbar()
        else:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.scatter_size, marker=self.scatter_marker, facecolors=self.scatter_facecolors,
                                         color=self.color,
                                         alpha=self.scatter_alpha)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 20)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)
            self.color_rule = self.z


class surface(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, surface_rstride=1, surface_cstride=1, surface_wire_width=0.1,
                 surface_lighting=False, surface_antialiased=False, surface_shade=False, surface_alpha=1,
                 surface_cmap_lighting=None, surface_norm=None,
                 surface_edge_color='black', surface_edges_to_rgba=False,
                 # Specifics: color
                 cmap='RdBu_r', color=None, color_rule=None,
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
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font_typeface=None, font_family='serif', font_math="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font='Latin Modern Roman',
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_bounds_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_bounds_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_bounds_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Surface class
        mpl_plotter - 3D

        Important combinations:
            Wireframe: alpha=0, line_width>0, surface_edges_to_rgba=False

        Specifics

        - Surface
        :param x: x
        :param y: y
        :param z: z
        :param surface_rstride: Surface grid definition
        :param surface_cstride: Surface grid definition
        :param line_width: Width of interpolating lines

        - Lighting
        :param surface_lighting: Apply lighting
        :param surface_antialiased: Apply antialiasing
        :param surface_shade: Apply shading

        - Color
        :param surface_norm: Instance of matplotlib.colors.Normalize.
            surface_norm = matplotlib.colors.Normalize(vmin=<vmin>, vmax=<vmax>)
        :param surface_edge_color: Color of surface plot edges
        :param surface_edges_to_rgba: Remove lines from surface plot
        :param alpha: Transparency
        :param cmap: Colormap
        :param surface_cmap_lighting: Colormap used for lighting

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
        for item in inspect.signature(surface).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):
        
        kwargs = {
            "alpha":          self.surface_alpha,
            "edgecolors":     self.surface_edge_color,
            "rstride":        self.surface_rstride,
            "cstride":        self.surface_cstride,
            "linewidth":      self.surface_wire_width,
            "antialiased":    self.surface_antialiased,
            "shade":          self.surface_shade
        }
        
        if self.surface_lighting:
            kwargs.update({
                "cmap":       self.cmap if self.color is None else None,
                "norm":       self.surface_norm,
                "color":      self.color,
                "facecolors": self.method_lighting()
            })
        elif self.color_rule is not None:
            kwargs.update({
                "cmap":       mpl.cm.get_cmap(self.cmap) if not isinstance(self.cmap, mpl.colors.LinearSegmentedColormap) else self.cmap,
                "norm":       self.surface_norm,
                "facecolors": cmap((self.color_rule + abs(self.color_rule.min()))/(self.color_rule.max() + abs(self.color_rule.min())))
            })
        elif self.surface_norm is not None:
            kwargs.update({
                "cmap":       self.cmap,
                "norm":       self.surface_norm
            })
        else:
            kwargs.update({
                "color":      self.color
            })

        self.graph = self.ax.plot_surface(self.x, self.y, self.z, **kwargs)
            
        self.method_colorbar()
        self.method_edges_to_rgba()

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x, self.y, self.z = MockData().hill()
            self.surface_norm = self.cb_norm = mpl.colors.Normalize(vmin=self.z.min(), vmax=self.z.max())

    def method_lighting(self):
        
        ls = LightSource(270, 45)

        if self.color is not None:
            if self.surface_cmap_lighting is None:
                try:
                    cmap = difflib.get_close_matches(self.color, self.plt.colormaps())[0]
                    print(f'You have selected the solid **color** "{self.color}" for your surface, and set **lighting** as **True**\n\n'
                          f'   The search for Matplotlib colormaps similar to "{self.color}" has resulted in: \n')
                    print(f'       "{cmap}"\n')
                    print('   Specify a custom colormap for the lighting function with the **surface_cmap_lighting** attribute.\n'
                          '   NOTE: This will overrule your monochrome color, however. Set **lighting** to **False** if this is undesired.')
                except IndexError:
                    cmap = "Greys"
                    print(f'You have selected the solid _color_ "{self.color}" for your surface, and set _lighting_ as True\n\n'
                          f'   The search for Matplotlib colormaps similar to "{self.color}" has failed. Reverting to\n')
                    print(f'       "{cmap}"\n')
                    print('   Specify a custom colormap for the lighting function with the _surface_cmap_lighting_ attribute.\n'
                          '   NOTE: This will overrule your monochrome color, however. Set _lighting_ to False if this is undesired.')
            else:
                cmap = self.surface_cmap_lighting if self.surface_cmap_lighting is not None else self.cmap
        else:
            cmap = self.surface_cmap_lighting if self.surface_cmap_lighting is not None else self.cmap
            
        rgb = ls.shade(self.z,
                       cmap=cm.get_cmap(cmap),
                       vert_exag=0.1,
                       blend_mode='soft')

        return rgb

    def method_edges_to_rgba(self):
        if self.surface_edges_to_rgba is True:
            self.graph.set_edgecolors(self.graph.to_rgba(self.graph._A))

