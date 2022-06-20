# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Precision
---------
"""

from mpl_plotter.presets.preset import preset, two_d as _two_d, three_d as _three_d

_precision_2D = {
**preset(dim=2),
**{
    ## Figure, axes
    "figsize" : (10, 7.5),
    ## Spines
    "spines_removed" : None,
    ## Pads
    "pad_demo" : True,
    ## Labels
    "label_size_x" : 20,
    "label_size_y" : 20,
    ## Ticks
    "tick_number_x" : 30,
    "tick_number_y" : 30,
    ## Tick labels
    "tick_label_size_x" : 8,
    "tick_label_size_y" : 9,
    "tick_bounds_fit" : True,
    "tick_label_decimals_y" : 3,
    "tick_rotation_x" : 45,
    ## Legend
    "legend_size" : 15,
}}

_precision_3D = {
**preset(dim=3),
**{
    ## Figure, axis
    "figsize": (10, 7.5),
    ## Pads
    "pad_demo": True,
    ## Labels
    "label_size_x": 20,
    "label_size_x": 20,
    "label_size_y": 20,
    "label_pad_x": 30,
    "label_pad_y": 30,
    "label_pad_z": 30,
    ## Ticks
    "tick_number_x": 20,
    "tick_number_y": 20,
    "tick_number_z": 20,
    ## Tick labels
    "tick_label_size_x": 8,
    "tick_label_size_y": 8,
    "tick_label_size_z": 9,
    "tick_rotation_x": -45,
    "tick_rotation_y": 45,
    "tick_label_decimals_z": 3,
    "tick_label_pad_x": 4,
    "tick_label_pad_y": 4,
    "tick_label_pad_z": 15,
    ## Legend
    "legend_size": 15,
}}

two_d   = _two_d  (preset=_precision_2D)
three_d = _three_d(preset=_precision_3D)
