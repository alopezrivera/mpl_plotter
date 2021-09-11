# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np

from mpl_plotter.presets.custom import generate_preset_2d, two_d
from mpl_plotter.presets.custom import generate_preset_3d, three_d


from tests.setup import show, backend


class PresetTests(unittest.TestCase):

    def test_2d(self):
        """
        Preferred use:

            generate_preset_2d(preset_dest="presets", preset_name="MYPRESET2D", disable_warning=True, overwrite=False)

            my_plot = three_d(preset_dir="presets", preset_name="MYPRESET2D").line

        Use to enable testing:
        """
        from tests.presets.MYPRESET2D import preset
        my_fam = two_d(preset=preset)

        my_fam.line(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.scatter(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.heatmap(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.quiver(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.streamline(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.fill_area(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")

    def test_3d(self):
        """
        Preferred use:

            generate_preset_3d(preset_dest="presets", preset_name="MYPRESET3D", disable_warning=True, overwrite=False)

            my_plot = three_d(preset_dir="presets", preset_name="MYPRESET3D").line

        Use to enable testing:
        """
        from tests.presets.MYPRESET3D import preset
        my_fam = three_d(preset=preset)

        my_fam.line(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.scatter(show=show, backend=backend, demo_pad_plot=True, color="blue", title="TITLE")
        my_fam.surface(show=show, backend=backend,
                       title="TITLE")

        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        x, y = np.meshgrid(x, y)
        z = np.sin(x ** 2 + y ** 2)
        my_fam.surface(x, y, z,
                       show=show, backend=backend,
                       demo_pad_plot=True,
                       title="TITLE",
                       azim=-58, elev=28,
                       lighting=True, shade=True, line_width=0)
        my_fam.surface(x, y, z,
                       show=show, backend=backend,
                       demo_pad_plot=True,
                       title="TITLE",
                       azim=-58, elev=28,
                       color="orange", line_width=0)
        my_fam.surface(x, y, z,
                       show=show, backend=backend,
                       demo_pad_plot=True,
                       title="TITLE",
                       azim=-58, elev=28,
                       color="orange",
                       lighting=True, shade=True, line_width=0)
        my_fam.surface(x, y, z,
                       show=show, backend=backend,
                       demo_pad_plot=True,
                       title="TITLE",
                       azim=-58, elev=28,
                       color="black",
                       lighting=True, shade=True, line_width=0)
