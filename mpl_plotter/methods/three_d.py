# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
3D Methods
----------
"""

import warnings

import numpy as np
import matplotlib as mpl

from matplotlib import font_manager
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.utils import span, bounds

def method_setup(plot):
    if plot.fig is None:
        if not plot.plt.get_fignums():
            plot.method_figure()
        else:
            plot.fig = plot.plt.gcf()
            axes = plot.fig.axes
            for ax in axes:
                if ax.__class__.__name__ == 'Axes3DSubplot':
                    plot.ax = ax

    if plot.ax is None:
        plot.ax = plot.fig.add_subplot(plot.shape_and_position, adjustable='box', projection='3d')

    plot.ax.view_init(azim=plot.azim, elev=plot.elev)

    plot.axes = ['x', 'y', 'z']

def method_spines(plot):

    if plot.spines_juggled is not None:
        plot.ax.xaxis._axinfo['juggled'] = plot.spines_juggled
    else:
        plot.ax.xaxis._axinfo['juggled'] = (1, 0, 2)

def method_pane_fill(plot):
    # Pane fill - False by default
    plot.ax.xaxis.pane.fill = False
    plot.ax.yaxis.pane.fill = False
    plot.ax.zaxis.pane.fill = False
    # Pane color - transparent by default
    plot.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    plot.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    plot.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    if plot.pane_fill is not None:
        # Set pane fill to True if a color is provided
        plot.ax.xaxis.pane.fill = True if plot.pane_fill is not None else False
        plot.ax.yaxis.pane.fill = True if plot.pane_fill is not None else False
        plot.ax.zaxis.pane.fill = True if plot.pane_fill is not None else False
        # Set pane fill color to that specified
        plot.ax.xaxis.set_pane_color(mpl.colors.to_rgba(plot.pane_fill))
        plot.ax.yaxis.set_pane_color(mpl.colors.to_rgba(plot.pane_fill))
        plot.ax.zaxis.set_pane_color(mpl.colors.to_rgba(plot.pane_fill))

    # Set edge colors
    if plot.blend_edges:
        if plot.pane_fill is not None:
            spine_color = plot.pane_fill
        else:
            spine_color = (0, 0, 0, 0)
    else:
        spine_color = plot.spine_color

    plot.ax.xaxis.pane.set_edgecolor(spine_color if np.any(np.array(plot.remove_axis).flatten() == "x")
                                        else plot.background_color_plot)
    plot.ax.yaxis.pane.set_edgecolor(spine_color if np.any(np.array(plot.remove_axis).flatten() == "y")
                                        else plot.background_color_plot)
    plot.ax.zaxis.pane.set_edgecolor(spine_color if np.any(np.array(plot.remove_axis).flatten() == "z")
                                        else plot.background_color_plot)

def method_remove_axes(plot):

    if plot.remove_axis is not None:
        for axis in np.array(plot.remove_axis).flatten():
            if axis == "x":
                plot.ax.xaxis.line.set_lw(0.)
                plot.ax.set_xticks([])
            if axis == "y":
                plot.ax.yaxis.line.set_lw(0.)
                plot.ax.set_yticks([])
            if axis == "z":
                plot.ax.zaxis.line.set_lw(0.)
                plot.ax.set_zticks([])

def method_scale(plot):

    if all([ascale_x is not None for ascale_x in [plot.scale_x, plot.scale_y, plot.scale_z]]):
        # Scaling
        mascale_x = max([plot.scale_x, plot.scale_y, plot.scale_z])
        scale_x = plot.scale_x/mascale_x
        scale_y = plot.scale_y/mascale_x
        scale_z = plot.scale_z/mascale_x

        scale_matrix = np.diag([scale_x, scale_y, scale_z, 1])

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        plot.ax.get_proj = lambda: np.dot(Axes3D.get_proj(plot.ax), scale_matrix)

    elif plot.aspect_equal:
        # Aspect ratio of 1
        #
        # Due to the flawed Matplotlib 3D axis aspect ratio
        # implementation, the z axis will be shrunk if it is
        # the one with the highest span.
        # This a completely empirical conclusion based on
        # some testing, and so is the solution.
        # Reference: https://github.com/matplotlib/matplotlib/issues/1077/

        Z_CORRECTION_FACTOR = 1.4

        span_x = span(plot.bounds_x)
        span_y = span(plot.bounds_y)
        span_z = span(plot.bounds_z)*Z_CORRECTION_FACTOR

        ranges = np.array([span_x,
                            span_y,
                            span_z])
        max_range = ranges.max()
        min_range = ranges[ranges > 0].min()

        scale_x = max(span_x, min_range)/max_range
        scale_y = max(span_y, min_range)/max_range
        scale_z = max(span_z, min_range)/max_range

        scale_matrix = np.diag([scale_x, scale_y, scale_z, 1])

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        plot.ax.get_proj = lambda: np.dot(Axes3D.get_proj(plot.ax), scale_matrix)

def method_resize_axes(plot):
    if plot.resize_axes is True:

        plot.bounds_x, plot.pad_upper_x, plot.pad_lower_x = bounds(plot.x,
                                                                                    plot.bound_upper_x,
                                                                                    plot.bound_lower_x,
                                                                                    plot.pad_upper_x,
                                                                                    plot.pad_lower_x,
                                                                                    plot.bounds_x)
        plot.bounds_y, plot.pad_upper_y, plot.pad_lower_y = bounds(plot.y,
                                                                                    plot.bound_upper_y,
                                                                                    plot.bound_lower_y,
                                                                                    plot.pad_upper_y,
                                                                                    plot.pad_lower_y,
                                                                                    plot.bounds_y)
        plot.bounds_z, plot.pad_upper_z, plot.pad_lower_z = bounds(plot.z,
                                                                                    plot.bound_upper_z,
                                                                                    plot.bound_lower_z,
                                                                                    plot.pad_upper_z,
                                                                                    plot.pad_lower_z,
                                                                                    plot.bounds_z)

        if plot.pad_demo is True:
            pad_x = 0.05 * span(plot.bounds_x)
            plot.pad_upper_x = pad_x
            plot.pad_lower_x = pad_x
            pad_y = 0.05 * span(plot.bounds_y)
            plot.pad_upper_y = pad_y
            plot.pad_lower_y = pad_y
            pad_z = 0.05 * span(plot.bounds_z)
            plot.pad_upper_z = pad_z
            plot.pad_lower_z = pad_z

        # Set bounds ignoring warnings if bounds are equal
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            plot.ax.set_xlim3d(plot.bounds_x[0] - plot.pad_lower_x,
                                plot.bounds_x[1] + plot.pad_upper_x)
            plot.ax.set_ylim3d(plot.bounds_y[0] - plot.pad_lower_y,
                                plot.bounds_y[1] + plot.pad_upper_y)
            plot.ax.set_zlim3d(plot.bounds_z[0] - plot.pad_lower_z,
                                plot.bounds_z[1] + plot.pad_upper_z)

def method_grid(plot):
    if plot.grid:
        plot.plt.grid(linestyle=plot.grid_lines, color=plot.grid_color)
    else:
        plot.ax.grid(plot.grid)
    if not plot.show_axes:
        plot.plt.axis('off')

def method_legend(plot):
    if plot.legend is True:
        legend_font = font_manager.FontProperties(family=plot.font_typeface,
                                                    weight=plot.legend_weight,
                                                    style=plot.legend_style,
                                                    size=plot.legend_size+plot.font_size_increase)
        plot.legend = plot.fig.legend(loc=plot.legend_loc, prop=legend_font,
                                        handleheight=plot.legend_handleheight, ncol=plot.legend_columns)

def method_tick_locs(plot):
    # Tick number
    if plot.tick_number_x is not None:
        # Tick locations
        if not(plot.tick_bounds_x is None):
            low = plot.tick_bounds_x[0]
            high = plot.tick_bounds_x[1]
        else:
            low = plot.x.min()
            high = plot.x.max()
        # Set usual ticks
        if plot.tick_number_x > 1 and span(plot.x) != 0:
            ticklocs = np.linspace(low, high, plot.tick_number_x)
        # Special case: single tick
        else:
            ticklocs = np.array([low + (high - low)/2])
        plot.ax.set_xticks(ticklocs)
    if plot.tick_number_y is not None:
        # Tick locations
        if not (plot.tick_bounds_y is None):
            low = plot.tick_bounds_y[0]
            high = plot.tick_bounds_y[1]
        else:
            low = plot.y.min()
            high = plot.y.max()
        # Set usual ticks
        if plot.tick_number_y > 1 and span(plot.y) != 0:
            ticklocs = np.linspace(low, high, plot.tick_number_y)
        # Special case: single tick
        else:
            ticklocs = np.array([low + (high - low) / 2])
        plot.ax.set_yticks(ticklocs)
    if plot.tick_number_z is not None:
        # Tick locations
        if not (plot.tick_bounds_z is None):
            low = plot.tick_bounds_z[0]
            high = plot.tick_bounds_z[1]
        else:
            low = plot.z.min()
            high = plot.z.max()
        # Set usual ticks
        if plot.tick_number_z > 1 and span(plot.z) != 0:
            ticklocs = np.linspace(low, high, plot.tick_number_z)
        # Special case: single tick
        else:
            ticklocs = np.array([low + (high - low) / 2])
        plot.ax.set_zticks(ticklocs)

def method_tick_labels(plot):
    
    # Tick color
    if plot.tick_color is not None:
        plot.ax.tick_params(axis='both', color=plot.tick_color)

    # Float format
    float_format = lambda x: '%.' + str(x) + 'f'

    
    for axis in ['x', 'y', 'z']:

        # Spines
        getattr(plot.ax, f'{axis}axis').line.set_color(plot.spine_color if plot.spine_color is not None else plot.workspace_color)

        # Float format
        axis_tick_label_decimals = getattr(plot, f'tick_label_decimals_{axis}')
        getattr(plot.ax, f'{axis}axis').set_major_formatter(
            FormatStrFormatter(float_format(axis_tick_label_decimals if axis_tick_label_decimals is not None else plot.tick_label_decimals))
        )
        
        # Custom tick labels
        tick_labels = getattr(plot, f'tick_labels_{axis}')
        if tick_labels is not None:
            getattr(plot.ax, f'set_{axis}ticklabels')(tick_labels)
        
        # Tick label formatting
        for label in getattr(plot.ax, f'get_{axis}ticklabels')():
            # Tick label typeface
            label.set_fontname(plot.font_typeface)
            # Tick label color
            label.set_color(plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color)
            # Tick label size
            axis_tick_label_size = getattr(plot, f'tick_label_size_{axis}')
            label.set_fontsize((axis_tick_label_size if axis_tick_label_size is not None else plot.tick_label_size) + plot.font_size_increase)
            # Tick label rotation
            label.set_rotation(getattr(plot, f'tick_rotation_{axis}'))

        # Tick label pad
        tick_label_pad = getattr(plot, f'tick_label_pad_{axis}')
        if tick_label_pad is not None:
            plot.ax.tick_params(axis=axis, pad=tick_label_pad)

def method_title(plot):
    if plot.title is not None:

        plot.ax.set_title(plot.title,
                          y=plot.title_y,
                          fontname=plot.font if plot.title_font is None else plot.title_font,
                          weight=plot.title_weight,
                          color=plot.workspace_color if plot.title_color is None else plot.title_color,
                          size=plot.title_size+plot.font_size_increase)
        plot.ax.title.set_position((0.5, plot.title_y))

def method_axis_labels(plot):
    if plot.label_x is not None:
        plot.ax.set_xlabel(plot.label_x, fontname=plot.font_typeface, weight=plot.label_weight_x,
                            color=plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color,
                            size=plot.label_size_x+plot.font_size_increase, labelpad=plot.label_pad_x,
                            rotation=plot.label_rotation_x)

    if plot.label_y is not None:
        plot.ax.set_ylabel(plot.label_y, fontname=plot.font_typeface, weight=plot.label_weight_y,
                            color=plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color,
                            size=plot.label_size_y+plot.font_size_increase, labelpad=plot.label_pad_y,
                            rotation=plot.label_rotation_y)

    if plot.label_z is not None:
        plot.ax.set_zlabel(plot.label_z, fontname=plot.font_typeface, weight=plot.label_weight_z,
                            color=plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color,
                            size=plot.label_size_z+plot.font_size_increase, labelpad=plot.label_pad_z,
                            rotation=plot.label_rotation_z)
