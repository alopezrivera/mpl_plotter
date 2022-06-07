# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Preset
------
"""

import os
import sys
import toml
import inspect
from pathlib import Path
from importlib import util
from copy import deepcopy as dc

from mpl_plotter.two_d import line as line2, \
                              scatter as scatter2, \
                              heatmap as heatmap2, \
                              quiver as quiver2, \
                              streamline as streamline2, \
                              fill_area as fill_area2

from mpl_plotter.three_d import line as line3, \
                                scatter as scatter3, \
                                surface as surface3


class preset:
    """
    Preset object class
    """

    def __init__(self, plotter=None, dim=None, _dict=None):

        assert not (plotter is None and _dict is None and dim is None),  \
            'either an MPL Plotter plotting class, a chosen dimension (2 or 3) or an argument dictionary must be provided to instantiate a ``preset`` object'
        
        self.preset = self._dict_from_plotter(plotter) if plotter is not None else \
                      self._dict_from_dim(dim)         if dim     is not None else \
                      _dict

    def __getitem__(self, item):
        return self.preset[item]

    def __getattr__(self, item):
        return getattr(self.__dict__['preset'], item)

    def __eq__(self, o):

        assert isinstance(o, preset), 'the equality operator can only be used to compare ``preset`` instances'

        return self.preset == o.preset

    def save(self, file):
        """
        Save MPL Plotter preset in TOML format
        """

        # create directories in file path if they do not exist        
        Path(os.path.dirname(file)).mkdir(parents=True, exist_ok=True)

        _dict = dc(self.preset)
        for k, v in _dict.items():
            if v is None:
                _dict[k] = 'None'

        dump  = toml.dumps(_dict)
        lines = dump.split('\n')[:-1]
        klen  = max([len(key) for key in _dict.keys()]) + 1

        with open(file, 'w') as f:

            f.write('\n'.join(['["MPL PLOTTER PRESET"]\n',
                               '# This file has been generated automatically',
                               '# by MPL Plotter and will be parsed using the',
                               '# Python TOML library (https://github.com/uiri/toml).',
                               '# Edit the value of each argument at will, but be',
                               '# mindful not to change their format (importantly,',
                               '# in the case of lists, and "None", which *must* be written',
                               '# within quotes) to avoid parsing errors.\n\n']))

            for line in lines:

                k, v = line.split('=')
                k    = k + ' '*(klen - len(k))
                f.write(f'{k} = {v}' + ("\n" if lines.index(line) != len(lines) - 1 else ""))
                
    @classmethod
    def load(cls, file):
        """
        Load MPL Plotter preset from TOML file
        """
        with open(file, 'r') as f:
            _dict = toml.load(f)['MPL PLOTTER PRESET']
        
        for k, v in _dict.items():
            if v == 'None':
                _dict[k] = None
            if isinstance(v, list):
                _dict[k] = tuple(v)

        return preset(_dict=_dict)

    @classmethod
    def _dict_from_plotter(cls, plotter):
        """
        Generate a dictionary containing all general arguments of the
        given ``plotter`` and their default values.
        """

        signature = inspect.signature(plotter)
        _dict = {
            k: v.default
            for k, v in signature.parameters.items()
            if k not in ['self', 'x', 'y', 'z', 'u', 'v'] and k[:len(plotter.__name__)] != plotter.__name__
        }

        return _dict

    @classmethod
    def _dict_from_dim(cls, dim):

        plotters = {2: [line2, scatter2, heatmap2, quiver2, streamline2, fill_area2],
                    3: [line3, scatter3, surface3]}[dim]

        _dict = preset._dict_from_plotter(plotters[0])

        for plotter in plotters[1:]:

            _dict = {k: _dict[k] for k in set(_dict.keys()).intersection(preset._dict_from_plotter(plotter).keys())}

        return _dict


class two_d():
    """
    2D preset plotting methods
    """

    def __init__(self, preset):
        global preset2
        preset2 = preset

    class line(line2):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, **input)

    class scatter(scatter2):

        def __init__(self, x=None, y=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, **input)

    class heatmap(heatmap2):

        def __init__(self, x=None, y=None, z=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, z=z, **input)

    class quiver(quiver2):

        def __init__(self, x=None, y=None, u=None, v=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, u=u, v=v, **input)

    class streamline(streamline2):

        def __init__(self, x=None, y=None, u=None, v=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, u=u, v=v, **input)

    class fill_area(fill_area2):

        def __init__(self, x=None, y=None, z=None, **kwargs):

            input = {**preset2, **kwargs}

            super().__init__(x=x, y=y, z=z, **input)


class three_d:
    """
    3D preset plotting methods
    """

    def __init__(self, preset):
        global preset3
        preset3 = preset

    class line(line3):

        def __init__(self, x=None, y=None, z=None, **kwargs):

            input = {**preset3, **kwargs}

            super().__init__(x=x, y=y, z=z, **input)

    class scatter(scatter3):

        def __init__(self, x=None, y=None, z=None, **kwargs):

            input = {**preset3, **kwargs}

            super().__init__(x=x, y=y, z=z, **input)

    class surface(surface3):

        def __init__(self, x=None, y=None, z=None, **kwargs):

            input = {**preset3, **kwargs}

            super().__init__(x=x, y=y, z=z, **input)
