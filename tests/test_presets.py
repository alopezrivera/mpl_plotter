# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest

import numpy as np

from mpl_plotter.presets import preset

from mpl_plotter.two_d import line, scatter, heatmap, streamline, quiver, fill_area
from mpl_plotter.three_d import line as line3, scatter as scatter3, surface as surface3



class TestGeneralAPIs(unittest.TestCase):

    def test_general_APIs_2D(self):
        
        general_APIs_2D = [preset(plotter) for plotter in [line, scatter, heatmap, streamline, quiver, fill_area]]

        for i in range(len(general_APIs_2D)):
            assert general_APIs_2D[0].keys() == general_APIs_2D[i].keys()
        

    def test_general_APIs_3D(self):

        general_APIs_3D = [preset(plotter) for plotter in [scatter3, surface3, line3]]

        keys = lambda i: general_APIs_3D[i].keys()

        for i in range(len(general_APIs_3D)):

            assert keys(i) == keys(0) or set(keys(i)).issubset(keys(0))



class TestPreset(unittest.TestCase):

    def test_preset_from_class(self):

        _preset = preset(line)

    def test_preset_from_dim(self):

        _preset = preset(dim=2)

    def test_preset_save_and_load(self):

        _preset = preset(dim=2)

        _preset.save('tests/presets/test.toml')

        loaded_preset = preset.load('tests/presets/test.toml')

        assert _preset.keys() == loaded_preset.keys()

        for key in _preset.keys():

            if type(_preset[key]) != type(loaded_preset[key]):
                assert _preset[key] == list(loaded_preset[key])
            else:
                assert _preset[key] == loaded_preset[key]


class TestMPLPlotterPresets(unittest.TestCase):

    def test_publication(self):
        
        from mpl_plotter.presets.publication import two_d as pub_2D, three_d as pub_3D
        
        pub_2D.line(show=True)
        pub_2D.scatter(show=True)
        pub_2D.heatmap(show=True)
        pub_2D.quiver(show=True)
        pub_2D.streamline(show=True)
        pub_2D.fill_area(show=True)

        pub_3D.line(show=True)
        pub_3D.scatter(show=True)
        pub_3D.surface(show=True)

    def test_precision(self):

        from mpl_plotter.presets.precision import two_d as pre_2D, three_d as pre_3D
        
        pre_2D.line(show=True)
        pre_2D.scatter(show=True)
        pre_2D.heatmap(show=True)
        pre_2D.quiver(show=True)
        pre_2D.streamline(show=True)
        pre_2D.fill_area(show=True)

        pre_3D.line(show=True)
        pre_3D.scatter(show=True)
        pre_3D.surface(show=True)
