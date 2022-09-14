# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
2D Components
-------------
"""

import numpy as np
import matplotlib as mpl

# COMMON
from mpl_plotter.methods.common import method_backend, \
                                       method_figure, \
                                       method_colorbar, \
                                       method_fonts, \
                                       method_workspace_style, \
                                       method_background_color, \
                                       method_subplots_adjust, \
                                       method_save, \
                                       method_show 

# 2D
from mpl_plotter.methods.two_d import method_setup, \
                                      method_spines, \
                                      method_resize_axes, \
                                      method_grid, \
                                      method_legend, \
                                      method_tick_locs, \
                                      method_tick_labels, \
                                      method_title, \
                                      method_axis_labels

class canvas:

    # COMMON
    method_backend          = method_backend
    method_figure           = method_figure
    method_workspace_style  = method_workspace_style
    method_background_color = method_background_color
    method_subplots_adjust  = method_subplots_adjust
    method_save             = method_save
    method_show             = method_show

    # 2D
    method_setup            = method_setup
    method_spines           = method_spines


class framing:

    # 2D
    method_resize_axes      = method_resize_axes


class guides:

    # 2D
    method_colorbar         = method_colorbar
    method_grid             = method_grid
    method_legend           = method_legend
    method_tick_locs        = method_tick_locs
    method_tick_labels      = method_tick_labels


class text:

    # 2D
    method_fonts            = method_fonts
    method_title            = method_title
    method_axis_labels      = method_axis_labels
