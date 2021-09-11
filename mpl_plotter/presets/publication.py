# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Publication plotting methods
----------------------------
"""


from mpl_plotter.presets.custom import two_d, three_d
from mpl_plotter.presets.data.publication import preset2, preset3


two_d(preset=preset2)
three_d(preset=preset3)
