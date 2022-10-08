# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
2D Methods
----------
"""

import re
import warnings

import numpy as np
import matplotlib as mpl

from matplotlib import font_manager
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.utils import span, bounds, ensure_ndarray

def method_setup(plot):
    if plot.fig is None:
        if not plot.plt.get_fignums():
            plot.method_figure()
        else:
            plot.fig = plot.plt.gcf()
            plot.ax = plot.plt.gca()
            
    if plot.ax is None:
        plot.ax = plot.fig.add_subplot(plot.shape_and_position, adjustable='box')

def method_spines(plot):
    for spine in plot.ax.spines.values():
        spine.set_color(plot.spine_color if plot.spine_color is not None else plot.workspace_color)

    if plot.spines_removed is not None:
        for i in range(len(plot.spines_removed)):
            if plot.spines_removed[i] == 1:
                plot.ax.spines[["left", "bottom", "top", "right"][i]].set_visible(False)

    # Axis ticks
    left, bottom, top, right = plot.ticks_where
    # Tick labels
    labelleft, labelbottom, labeltop, labelright = plot.tick_labels_where

    plot.ax.tick_params(axis='both', which='both',
                        top=top, right=right, left=left, bottom=bottom,
                        labeltop=labeltop, labelright=labelright, labelleft=labelleft, labelbottom=labelbottom)

def method_resize_axes(plot):

    # Bound definition
    if plot.bounds_x is not None:
        if plot.bounds_x[0] is not None:
            plot.bound_lower_x = plot.bounds_x[0]
        if plot.bounds_x[1] is not None:
            plot.bound_upper_x = plot.bounds_x[1]
    if plot.bounds_y is not None:
        if plot.bounds_y[0] is not None:
            plot.bound_lower_y = plot.bounds_y[0]
        if plot.bounds_y[1] is not None:
            plot.bound_lower_y = plot.bounds_y[1]

    if plot.resize_axes and plot.x.size != 0 and plot.y.size != 0:

        plot.bounds_x, plot.pad_upper_x, plot.pad_lower_x = bounds(plot.x,
                                                                   plot.bound_upper_x,
                                                                   plot.bound_lower_x,
                                                                   plot.pad_upper_x,
                                                                   plot.pad_lower_x,
                                                                   plot.bounds_x)
        plot.bounds_y, plot.pad_upper_y, plot.pad_lower_y = bounds(plot.y,
                                                                   plot.bound_lower_y,
                                                                   plot.bound_lower_y,
                                                                   plot.pad_upper_y,
                                                                   plot.pad_lower_y,
                                                                   plot.bounds_y)
        
        # Aspect and scale
        if plot.scale is not None and plot.aspect is not None:
            # mean value of the data
            mean = lambda ax: np.array(getattr(plot, f'bounds_{ax}')).mean()
            # half-span, adjusted for scale and aspect ratio
            buff = lambda ax: span(getattr(plot, f'bounds_{ax}'))/2 * (1/plot.scale/plot.aspect if ax == 'y' else plot.scale*plot.aspect)
            if span(plot.bounds_x) > span(plot.bounds_y):
                plot.bounds_y = [mean('y') - buff('x'), mean('y') + buff('x')]
            else:
                plot.bounds_x = [mean('x') - buff('y'), mean('x') + buff('y')]

        # Room to breathe
        if plot.pad_demo:
            pad_x = 0.05 * span(plot.bounds_x)
            plot.pad_upper_x = pad_x
            plot.pad_lower_x = pad_x
            pad_y = 0.05 * span(plot.bounds_y)
            plot.pad_upper_y = pad_y
            plot.pad_lower_y = pad_y

        # Allow constant input and single coordinate plots
        # Single coordinate plots
        if span(plot.bounds_x) == 0 and span(plot.bounds_y) == 0:
            # x bounds
            plot.bounds_x = [plot.x - plot.x/2, plot.x + plot.x/2]
            plot.pad_upper_x = 0
            plot.pad_lower_x = 0
            # y bounds
            plot.bounds_y = [plot.y - plot.y/2, plot.y + plot.y/2]
            plot.pad_upper_y = 0
            plot.pad_lower_y = 0
        # Constant x coordinate plot
        elif span(plot.bounds_x) == 0:
            plot.bounds_x = [plot.x[0] - span(plot.y)/2, plot.x[0] + span(plot.y)/2]
            plot.pad_upper_x = plot.pad_upper_y
            plot.pad_lower_x = plot.pad_lower_y
        # Constant y coordinate plot
        elif span(plot.bounds_y) == 0:
            plot.bounds_y = [plot.y[0] - span(plot.x)/2, plot.y[0] + span(plot.x)/2]
            plot.pad_upper_y = plot.pad_upper_x
            plot.pad_lower_y = plot.pad_lower_x

        # Set bounds ignoring warnings if bounds are equal
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            plot.ax.set_xbound(lower=plot.bounds_x[0] - plot.pad_lower_x,
                                upper=plot.bounds_x[1] + plot.pad_upper_x)
            plot.ax.set_ybound(lower=plot.bounds_y[0] - plot.pad_lower_y,
                                upper=plot.bounds_y[1] + plot.pad_upper_y)

            plot.ax.set_xlim(plot.bounds_x[0] - plot.pad_lower_x,
                                plot.bounds_x[1] + plot.pad_upper_x)
            plot.ax.set_ylim(plot.bounds_y[0] - plot.pad_lower_y,
                                plot.bounds_y[1] + plot.pad_upper_y)

        # Aspect ratio
        if plot.aspect is not None and span(plot.bounds_x) != 0 and span(plot.bounds_y) != 0:
            y_range = span(plot.bounds_y)
            x_range = span(plot.bounds_x)

            aspect = x_range/y_range * plot.aspect

            plot.ax.set_aspect(aspect)

        # Scale
        if plot.scale is not None:
            plot.ax.set_aspect(plot.scale)

def method_grid(plot):
    if plot.grid:
        plot.ax.grid(linestyle=plot.grid_lines, color=plot.grid_color)

def method_legend(plot):
    if plot.legend:
        lines_labels = [ax.get_legend_handles_labels() for ax in plot.fig.axes]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        legend_font = font_manager.FontProperties(family=plot.font_typeface,
                                                  weight=plot.legend_weight,
                                                  style=plot.legend_style,
                                                  size=plot.legend_size + plot.font_size_increase)
        plot.legend = plot.fig.legend(lines, labels,
                                        loc=plot.legend_loc,
                                        bbox_to_anchor=plot.legend_bbox_to_anchor, prop=legend_font,
                                        handleheight=plot.legend_handleheight, ncol=plot.legend_ncol)

def method_tick_locs(plot):
    # ----------------
    # Input validation
    # ----------------
    # Avoid issues with arrays with span 0 (vertical or horizontal lines)
    if plot.x is not None and plot.y is not None:
        if plot.tick_bounds_fit:
            if plot.tick_bounds_x is None:
                plot.tick_bounds_x = [plot.x.min(), plot.x.max()] if plot.x.size != 0 else [-1, 1]
            if plot.tick_bounds_y is None:
                plot.tick_bounds_y = [plot.y.min(), plot.y.max()] if plot.y.size != 0 else [-1, 1]
    # Ensure the number of ticks equals the length of the list of
    # tick labels, if provided
    if plot.tick_labels_x is not None:                   
        if plot.tick_number_x != len(plot.tick_labels_x):
            plot.tick_number_x = len(plot.tick_labels_x) 
    if plot.tick_labels_y is not None:
        if plot.tick_number_y != len(plot.tick_labels_y):        # length of the list of custom tick
            plot.tick_number_y = len(plot.tick_labels_y)         # labels.

    # ----------------
    #  Implementation
    # ----------------
    if not plot.tick_locations_x is None:
        # Custom tick locations
        if not plot.tick_locations_x is None:
            plot.ax.set_xticks(ensure_ndarray(plot.tick_locations_x))
    else:
        # Along bounds
        high = plot.tick_bounds_x[0]
        low  = plot.tick_bounds_x[1]
        if plot.tick_number_x == 1:
            # Single tick
            ticklocs = np.array([low + (high - low)/2])
        else:
            ticklocs = np.linspace(low, high, plot.tick_number_x)
            plot.ax.set_xticks(ticklocs)
    
    if not plot.tick_locations_y is None:
        # Custom tick locations
        if not plot.tick_locations_y is None:
            plot.ax.set_yticks(ensure_ndarray(plot.tick_locations_y))
    else:
        # Along bounds
        high = plot.tick_bounds_y[0]
        low  = plot.tick_bounds_y[1]
        if plot.tick_number_y == 1:
            # Single tick
            ticklocs = np.array([low + (high - low)/2])
        else:
            ticklocs = np.linspace(low, high, plot.tick_number_y)
            plot.ax.set_yticks(ticklocs)

def method_tick_labels(plot):
    # ----------------
    #      Ticks
    # ----------------

    # Tick-axis pad
    plot.ax.xaxis.set_tick_params(pad=0.1, direction='in')
    plot.ax.yaxis.set_tick_params(pad=0.1, direction='in')

    # Tick color
    if plot.tick_color is not None:
        plot.ax.tick_params(axis='both', color=plot.tick_color)

    # ----------------
    #     Position
    # ----------------
    
    # Tick-label pad
    if plot.tick_label_pad is not None:
        plot.ax.tick_params(axis='both', pad=plot.tick_label_pad)
    
    # ----------------
    #      Format
    # ----------------
    
    # Font and color
    for tick in plot.ax.get_xticklabels():
        tick.set_fontname(plot.font_typeface)
        tick.set_color(plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color)
    for tick in plot.ax.get_yticklabels():
        tick.set_fontname(plot.font_typeface)
        tick.set_color(plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color)

    # Label size
    if plot.tick_label_size_x is not None:
        plot.ax.tick_params(axis='x', labelsize=plot.tick_label_size_x + plot.font_size_increase)
    elif plot.tick_label_size is not None:
        plot.ax.tick_params(axis='x', labelsize=plot.tick_label_size + plot.font_size_increase)
    if plot.tick_label_size_y is not None:
        plot.ax.tick_params(axis='y', labelsize=plot.tick_label_size_y + plot.font_size_increase)
    elif plot.tick_label_size is not None:
        plot.ax.tick_params(axis='y', labelsize=plot.tick_label_size + plot.font_size_increase)

    # Rotation
    if plot.tick_rotation_x is not None:
        plot.ax.tick_params(axis='x', rotation=plot.tick_rotation_x)
        for tick in plot.ax.xaxis.get_majorticklabels():
            tick.set_horizontalalignment("right")
    if plot.tick_rotation_y is not None:
        plot.ax.tick_params(axis='y', rotation=plot.tick_rotation_y)
        for tick in plot.ax.yaxis.get_majorticklabels():
            tick.set_horizontalalignment("left")
            
    # ----------------
    #     Content
    # ----------------

    # Decimals - must be set BEFORE setting plot.tick_labels_<>
    decimals_x = plot.tick_label_decimals_x if plot.tick_label_decimals_x is not None else plot.tick_label_decimals
    decimals_y = plot.tick_label_decimals_y if plot.tick_label_decimals_y is not None else plot.tick_label_decimals
    float_format_x = '%.' + str(decimals_x) + 'f'
    float_format_y = '%.' + str(decimals_y) + 'f'
    plot.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format_x))
    plot.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format_y))
    
    # Custom tick labels
    if plot.tick_labels_x is not None:
        if len(plot.tick_labels_x) == 2 and len(plot.tick_labels_x) != plot.tick_number_x:
            plot.tick_labels_x = np.linspace(plot.tick_labels_x[0],
                                                    plot.tick_labels_x[1],
                                                    plot.tick_number_x)
        plot.ax.set_xticklabels(plot.tick_labels_x[::-1])
        
    if plot.tick_labels_y is not None:
        if len(plot.tick_labels_y) == 2 and len(plot.tick_labels_y) != plot.tick_number_y:
            plot.tick_labels_y = np.linspace(plot.tick_labels_y[0],
                                                    plot.tick_labels_y[1],
                                                    plot.tick_number_y)
        plot.ax.set_yticklabels(plot.tick_labels_y[::-1])

    # Date tick labels
    if plot.tick_labels_dates_x:
        fmtd = pd.date_range(start=plot.x[0], end=plot.x[-1], periods=plot.tick_number_x)
        fmtd = [dt.datetime.strftime(d, plot.date_format) for d in fmtd]
        plot.ax.set_xticklabels(fmtd)

def method_title(plot):
    if plot.title is not None:

        for c in [plot.title_color, plot.font_color, plot.workspace_color]:
            if c is not None:
                color = c
                break
            
        plot.ax.set_title(plot.title,
                          fontname=plot.title_font if plot.title_font is not None else plot.font_typeface,
                          weight=plot.title_weight,
                          color=color,
                          size=plot.title_size + plot.font_size_increase,
                          pad=plot.title_pad)

def method_axis_labels(plot):
    if plot.label_x is not None:

        # Draw label
        plot.ax.set_xlabel(plot.label_x, fontname=plot.font_typeface, weight=plot.label_weight_x,
                            color=plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color,
                            size=plot.label_size_x + plot.font_size_increase, labelpad=plot.label_pad_x,
                            rotation=plot.label_rotation_x)

        # Custom coordinates if provided
        if plot.label_coords_x is not None:
            plot.ax.xaxis.set_label_coords(x=plot.label_coords_x[0], y=plot.label_coords_x[1])

    if plot.label_y is not None:

        # y axis label rotation
        if plot.label_rotation_y is None:
            latex_chars  = re.findall(r'\$\\(.*?)\$', plot.label_y)
            label_length = len(plot.label_y) - 2*len(latex_chars) - len(''.join(latex_chars).replace('//', '/'))
            plot.label_rotation_y = 90 if label_length > 3 else 0

        # Draw label
        plot.ax.set_ylabel(plot.label_y, fontname=plot.font_typeface, weight=plot.label_weight_y,
                            color=plot.workspace_color if plot.font_color == plot.workspace_color else plot.font_color,
                            size=plot.label_size_y + plot.font_size_increase, labelpad=plot.label_pad_y,
                            rotation=plot.label_rotation_y)

        # Custom coordinates if provided
        if plot.label_coords_y is not None:
            plot.ax.yaxis.set_label_coords(x=plot.label_coords_y[0], y=plot.label_coords_y[1])
