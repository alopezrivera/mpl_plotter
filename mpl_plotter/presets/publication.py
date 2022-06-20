# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Publication
-----------
"""

from mpl_plotter.presets.preset import preset, two_d as _two_d, three_d as _three_d

_publication_2D = {
**preset(dim=2),
**{
    ## Figure, axes
    "figsize"               : (5, 5),
    "aspect"                : 1,
    "scale"                 : None,
    ## Spines
    "spines_removed"        : (0, 0, 1, 1),
    ## Pads
    "pad_demo"              : True,
    ## Labels
    "label_size_x"          : 20,
    "label_size_y"          : 20,
    ## Ticks
    "tick_number_x"         : 3,
    "tick_number_y"         : 3,
    ## Tick labels
    "tick_label_size_x"     : 15,
    "tick_label_size_y"     : 15,
    "tick_bounds_fit"   : True,
    "tick_label_decimals_y" : 3,
    ## Legend
    "legend_size"           : 15,
    ## Subplots
    "top"                   : 0.975,
    "bottom"                : 0.085,
    "left"                  : 0.230,
    "right"                 : 0.87,
    "hspace"                : 0.2,
    "wspace"                : 0.2,
}}

_publication_3D = {
**preset(dim=3),
**{
    ## Figure, axis
    "figsize"               : (6, 6),
    ## Pads
    "pad_demo"              : True,
    ## Labels
    "label_size_x"          : 20,
    "label_size_y"          : 20,
    "label_size_z"          : 20,
    "label_pad_x"           : 10,
    "label_pad_y"           : 10,
    "label_pad_z"           : 20,
    "label_weight_x"        : "bold",
    "label_weight_y"        : "bold",
    "label_weight_z"        : "bold",
    ## Ticks
    "tick_number_x"         : 3,
    "tick_number_y"         : 3,
    "tick_number_z"         : 3,
    ## Tick labels
    "tick_label_size_x"     : 15,
    "tick_label_size_y"     : 15,
    "tick_label_size_z"     : 15,
    "tick_label_decimals_z" : 3,
    "tick_label_pad_x"      : 4,
    "tick_label_pad_y"      : 4,
    "tick_label_pad_z"      : 10,
    ## Legend
    "legend_size"           : 15,
    ## Subplots
    "top"                   : 0.975,
    "bottom"                : 0.085,
    "left"                  : 0.14,
    "right"                 : 0.945,
    "hspace"                : 0.2,
    "wspace"                : 0.2,
}}

two_d   = _two_d  (preset=_publication_2D)
three_d = _three_d(preset=_publication_3D)
