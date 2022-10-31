# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Placeholders
------------
"""

import numpy as np
from matplotlib import cbook


def hill():
    with cbook.get_sample_data('jacksboro_fault_dem.npz', np_load=True) as dem:
        z = dem['elevation']
        nrows, ncols = z.shape
        x = np.linspace(dem['xmin'], dem['xmax'], ncols)
        y = np.linspace(dem['ymin'], dem['ymax'], nrows)
        x, y = np.meshgrid(x, y)

    region = np.s_[5:50, 5:50]
    x, y, z = x[region], y[region], z[region]

    return x, y, z
