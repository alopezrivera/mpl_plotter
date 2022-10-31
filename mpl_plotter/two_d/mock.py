# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Placeholders
------------
"""


import numpy as np
import pandas as pd

from numpy import sin, cos


def diff_field():
    x1 = np.linspace(-2, 2, 250)
    x2 = np.linspace(-2, 2, 250)
    x1, x2 = np.meshgrid(x1, x2)

    dx1 = x1**2-x2**3
    dx2 = 2*x1*(x1**2-x2)
            
    dx = np.log10(np.sqrt(dx1**2+dx2**2))

    return x1, x2, dx1, dx2, dx

def spirograph():
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

def waterdrop():

    d = 1000

    x = np.linspace(-3, 3, d)
    y = np.linspace(-3, 3, d)

    x, y = np.meshgrid(x, y)

    z = -(1 + cos(12 * np.sqrt(x * x + y * y))) / (0.5 * (x * x + y * y) + 2)

    return x, y, z

def boltzmann(x, xmid, tau):
    """
    Evaluate the boltzman function with midpoint xmid and time constant tau over x
    """
    return 1 / (1 + np.exp(-(x - xmid) / tau))
