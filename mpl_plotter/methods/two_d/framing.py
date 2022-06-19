# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Framing
-------
"""

import warnings

from mpl_plotter.utils import span


class framing:

    def method_resize_axes(self):

        # Bound definition
        if self.bounds_x is not None:
            if self.bounds_x[0] is not None:
                self.bound_lower_x = self.bounds_x[0]
            if self.bounds_x[1] is not None:
                self.bound_upper_x = self.bounds_x[1]
        if self.bounds_y is not None:
            if self.bounds_y[0] is not None:
                self.bound_lower_y = self.bounds_y[0]
            if self.bounds_y[1] is not None:
                self.bound_lower_y = self.bounds_y[1]

        if self.resize_axes and self.x.size != 0 and self.y.size != 0:

            def bounds(d, u, l, up, lp, v):
                # Upper and lower bounds
                if isinstance(u, type(None)):
                    u = d.max()
                else:
                    up = 0
                if isinstance(l, type(None)):
                    l = d.min()
                else:
                    lp = 0
                # Bounds vector
                if isinstance(v, type(None)):
                    v = [l, u]
                if isinstance(v[0], type(None)):
                    v[0] = l
                if isinstance(v[1], type(None)):
                    v[1] = u
                return v, up, lp

            self.bounds_x, self.pad_upper_x, self.pad_lower_x = bounds(self.x,
                                                                                     self.bound_upper_x,
                                                                                     self.bound_lower_x,
                                                                                     self.pad_upper_x,
                                                                                     self.pad_lower_x,
                                                                                     self.bounds_x)
            self.bounds_y, self.pad_upper_y, self.pad_lower_y = bounds(self.y,
                                                                                     self.bound_lower_y,
                                                                                     self.bound_lower_y,
                                                                                     self.pad_upper_y,
                                                                                     self.pad_lower_y,
                                                                                     self.bounds_y)

            # Room to breathe
            if self.pad_demo:
                pad_x = 0.05 * span(self.bounds_x)
                self.pad_upper_x = pad_x
                self.pad_lower_x = pad_x
                pad_y = 0.05 * span(self.bounds_y)
                self.pad_upper_y = pad_y
                self.pad_lower_y = pad_y

            # Allow constant input and single coordinate plots
            # Single coordinate plots
            if span(self.bounds_x) == 0 and span(self.bounds_y) == 0:
                # x bounds
                self.bounds_x = [self.x - self.x/2, self.x + self.x/2]
                self.pad_upper_x = 0
                self.pad_lower_x = 0
                # y bounds
                self.bounds_y = [self.y - self.y/2, self.y + self.y/2]
                self.pad_upper_y = 0
                self.pad_lower_y = 0
            # Constant x coordinate plot
            elif span(self.bounds_x) == 0:
                self.bounds_x = [self.x[0] - span(self.y)/2, self.x[0] + span(self.y)/2]
                self.pad_upper_x = self.pad_upper_y
                self.pad_lower_x = self.pad_lower_y
            # Constant y coordinate plot
            elif span(self.bounds_y) == 0:
                self.bounds_y = [self.y[0] - span(self.x)/2, self.y[0] + span(self.x)/2]
                self.pad_upper_y = self.pad_upper_x
                self.pad_lower_y = self.pad_lower_x

            # Set bounds ignoring warnings if bounds are equal
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                self.ax.set_xbound(lower=self.bounds_x[0] - self.pad_lower_x,
                                   upper=self.bounds_x[1] + self.pad_upper_x)
                self.ax.set_ybound(lower=self.bounds_y[0] - self.pad_lower_y,
                                   upper=self.bounds_y[1] + self.pad_upper_y)

                self.ax.set_xlim(self.bounds_x[0] - self.pad_lower_x,
                                 self.bounds_x[1] + self.pad_upper_x)
                self.ax.set_ylim(self.bounds_y[0] - self.pad_lower_y,
                                 self.bounds_y[1] + self.pad_upper_y)

            # Aspect ratio
            if self.aspect is not None and span(self.bounds_x) != 0 and span(self.bounds_y) != 0:
                y_range = span(self.bounds_y)
                x_range = span(self.bounds_x)

                aspect = x_range/y_range * self.aspect

                self.ax.set_aspect(aspect)

            # Scale
            if self.scale is not None:
                self.ax.set_aspect(self.scale)

