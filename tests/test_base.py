# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest
import numpy as np


from tests.setup import show, backend


class TestAll(unittest.TestCase):

    def test_two_d(self):
        from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area

        line(show=show, backend=backend)
        
        scatter(show=show, backend=backend)

        heatmap(show=show, backend=backend)

        quiver(show=show, backend=backend)

        streamline(show=show, backend=backend)
        
        fill_area(show=show, backend=backend)        

        # title
        scatter(show=show, backend=backend,
                title='A Title including math: $\int_a^bxdx$',
                title_pad=20,
                top=0.815,
                bottom=0.105,
                left=0.165,
                right=0.87,
                hspace=0.2,
                wspace=0.2)

    def test_two_d_cb(self):
        from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area
        
        line(show=show, backend=backend,
             color_rule=True,
             colorbar=True,
             cb_shrink=0.75)
        
        scatter(show=show, backend=backend,
                colorbar=True,
                cb_shrink=0.75)

        heatmap(show=show, backend=backend,
                colorbar=True,
                cb_shrink=0.75)

        quiver(show=show, backend=backend,
               colorbar=True,
               cb_shrink=0.75)

        streamline(show=show, backend=backend,
                   colorbar=True,
                   cb_shrink=0.75)

        colorbar = {
            'colorbar':                 True,
            'cb_orientation':           'horizontal',
            'cb_hard_bounds':           False,
            'cb_outline_width':         0.5,
            'cb_extend':                'both',
            'cb_tick_label_decimals':   1,
        }

        colorbar_title_floating = {
            'cb_title':                 'Color Bar',
            'cb_title_font':            'Century Gothic',
            'cb_title_weight':          'bold',
            'cb_title_floating':        True,
            'cb_title_floating_coords': [0.4, 1.3],
        }

        colorbar_title_anchored = {
            'cb_title':                 'Color Bar',
            'cb_title_font':            'Century Gothic',
            'cb_title_weight':          'bold',
        }
        
        # floating colorbar
        scatter(show=show, backend=backend,

                **colorbar,
                **colorbar_title_floating,

                cb_floating=True, cb_floating_coords=[0.24, 0.075], cb_floating_dimensions=[0.55, 0.03],

                top=0.93,
                bottom=0.21,
                left=0.165,
                right=0.87,
                hspace=0.2,
                wspace=0.2
                )
        
        # side colorbar
        scatter(show=show, backend=backend,
                
                **colorbar,
                **colorbar_title_anchored,
                
                cb_anchored_pad=0.1,
                cb_shrink=0.75,
                
                top=0.93,
                bottom=0.00,
                left=0.165,
                right=0.87,
                hspace=0.2,
                wspace=0.2
                )

    def test_three_d(self):
        from mpl_plotter.three_d import line, scatter, surface

        line(show=show, backend=backend)

        scatter(show=show, backend=backend)

        surface(show=show, backend=backend)

        # title
        scatter(show=show, backend=backend,
                title='A Title including math: $\int_a^bxdx$',
                # title_pad=20,
                top=0.815,
                bottom=0.105,
                left=0.165,
                right=0.87,
                hspace=0.2,
                wspace=0.2)

        # color bar
        scatter(show=show, backend=backend,
                colorbar=True,
                cb_title="Color Bar",
                # cb_title_side=True,
                cb_tick_label_decimals=1,
                # cb_hard_bounds=True,
                cb_orientation='horizontal',
                cb_anchored_pad=0.075,
                cb_shrink=0.7)

        # wireframe
        surface(show=show, backend=backend, 
                surface_alpha=0,
                surface_wire_width=0.5,
                surface_edge_color="red",
                surface_cstride=12,
                surface_rstride=12)

        # solid color
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        x, y = np.meshgrid(x, y)
        z = np.sin(x**2 + y**2)
        surface(x, y, z,
                color="orange",
                surface_wire_width=0,
                surface_lighting=True,
                show=show, backend=backend)

    def test_three_d_cb(self):
        from mpl_plotter.three_d import scatter, surface

        scatter(show=show, backend=backend,
                colorbar=True,
                cb_shrink=0.65)

        surface(show=show, backend=backend,
                colorbar=True,
                cb_shrink=0.65)
