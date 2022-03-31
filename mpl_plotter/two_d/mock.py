# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Placeholders
------------
"""


import numpy as np
import pandas as pd

from numpy import sin, cos


class MockData:

    def filled_julia(self, xyz_2d=False, xyz_3d=False, df=False):
        w, h, zoom = 1920, 1920, 1
        cX, cY = -0.7, 0.27015
        moveX, moveY = 0.0, 0.0
        maxIter = 255

        z = np.zeros(shape=(w, h))

        for x in range(w):
            for y in range(h):
                zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
                zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
                i = maxIter
                while zx * zx + zy * zy < 4 and i > 1:
                    tmp = zx * zx - zy * zy + cX
                    zy, zx = 2.0 * zx * zy + cY, tmp
                    i -= 1

                z[x, y] = (i << 21) + (i << 10) + i * 8

        x = np.linspace(0, w, w)
        y = np.linspace(0, h, h)

        if xyz_2d is True:
            return x, y, z

        if xyz_3d is True:
            x, y = np.meshgrid(x, y)
            return x, y, z

        if df is True:
            return pd.DataFrame(z)

        return np.linspace(0, w, w), np.linspace(0, h, h), z

    def spirograph(self):
        # Plot a spirograph
        R = 125
        d = 200
        r = 50
        dtheta = 0.2
        steps = 8 * int(6 * 3.14 / dtheta)
        x = np.zeros(shape=(steps, 1))
        y = np.zeros(shape=(steps, 1))
        theta = 0
        for step in range(0, steps):
            theta = theta + dtheta
            x[step] = (R - r) * cos(theta) + d * cos(((R - r) / r) * theta)
            y[step] = (R - r) * sin(theta) - d * sin(((R - r) / r) * theta)

        return x.flatten(), y.flatten()

    def sinewave(self):
        steps = 100
        x_max = 215
        x = np.linspace(-x_max, x_max, steps)
        y = 50 * np.sin(2 * np.pi * (x + x_max) / x_max)
        return x, y

    def waterdrop(self):

        d = 1000

        x = np.linspace(-3, 3, d)
        y = np.linspace(-3, 3, d)

        x, y = np.meshgrid(x, y)

        z = -(1 + cos(12 * np.sqrt(x * x + y * y))) / (0.5 * (x * x + y * y) + 2)

        return x, y, z

    def boltzman(self, x, xmid, tau):
        """
        Evaluate the boltzman function with midpoint xmid and time constant tau
        over x
        """
        return 1 / (1 + np.exp(-(x - xmid) / tau))
