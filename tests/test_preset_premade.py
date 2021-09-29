# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np

from mpl_plotter.color.schemes import colorscheme_one


x = np.linspace(0, 4, 1000)
y = np.exp(x)
z = abs(np.sin(x) * np.exp(x))


from tests.setup import show, backend


class Tests(unittest.TestCase):

    def test_publication2(self):
        from mpl_plotter.presets.publication import two_d
        two_d.line(x, z, color=colorscheme_one()[5], show=show, backend=backend)
        two_d.scatter(x, z, norm=z, show=show, backend=backend)
        two_d.heatmap(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.quiver(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.streamline(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.fill_area(color=colorscheme_one()[5], show=show, backend=backend)

    def test_precision2(self):
        from mpl_plotter.presets.precision import two_d
        two_d.line(x, z, color=colorscheme_one()[5], show=show, backend=backend)
        two_d.scatter(x, z, norm=z, show=show, backend=backend)
        two_d.heatmap(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.quiver(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.streamline(color=colorscheme_one()[5], show=show, backend=backend)
        two_d.fill_area(color=colorscheme_one()[5], show=show, backend=backend)


class Tests3(unittest.TestCase):

    def test_publication3(self):
        from mpl_plotter.presets.publication import three_d
        three_d.line(x, y, z, color=colorscheme_one()[5], show=show, backend=backend)
        three_d.scatter(x, y, z, color_rule=z, color=colorscheme_one()[5], show=show, backend=backend)
        three_d.surface(color=colorscheme_one()[5], show=show, backend=backend, demo_pad_plot=True)

    def test_precision3(self):
        from mpl_plotter.presets.precision import three_d
        three_d.line(x, y, z, color=colorscheme_one()[5], show=show, backend=backend)
        three_d.scatter(x, y, z, color_rule=z, color=colorscheme_one()[5], show=show, backend=backend)
        three_d.surface(color=colorscheme_one()[5], show=show, backend=backend, demo_pad_plot=True)
