# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Placeholders
------------
"""

import numpy as np
from matplotlib import cbook


class MockData:

    def waterdrop3d(self):
        d = 100

        x = np.linspace(-3, 3, d)
        y = np.linspace(-3, 3, d)

        x, y = np.meshgrid(x, y)

        z = -(1 + np.cos(12 * np.sqrt(x * x + y * y))) / (0.5 * (x * x + y * y) + 2)

        print(x.shape, y.shape)

        return x, y, z

    def random3d(self):
        np.random.seed(123)

        x, y = np.random.uniform(size=(100, 2)).T

        z = -(1 + np.cos(12 * np.sqrt(x * x + y * y))) / (0.5 * (x * x + y * y) + 2)

        return x, y, z

    def hill(self):
        with cbook.get_sample_data('jacksboro_fault_dem.npz', np_load=True) as dem:
            z = dem['elevation']
            nrows, ncols = z.shape
            x = np.linspace(dem['xmin'], dem['xmax'], ncols)
            y = np.linspace(dem['ymin'], dem['ymax'], nrows)
            x, y = np.meshgrid(x, y)

        region = np.s_[5:50, 5:50]
        x, y, z = x[region], y[region], z[region]

        return x, y, z