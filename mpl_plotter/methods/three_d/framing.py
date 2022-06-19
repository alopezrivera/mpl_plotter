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
        if self.resize_axes is True:

            def bounds(d, u, l, up, lp, v):
                # Upper and lower bounds
                if u is None:
                    u = d.max()
                else:
                    up = 0
                if l is None:
                    l = d.min()
                else:
                    lp = 0
                # Bounds vector
                if v is None:
                    v = [self.bound_lower_x, self.bound_upper_x]
                if v[0] is None:
                    v[0] = l
                if v[1] is None:
                    v[1] = u
                return v, up, lp

            self.bounds_x, self.pad_upper_x, self.pad_lower_x = bounds(self.x,
                                                                                     self.bound_upper_x,
                                                                                     self.bound_lower_x,
                                                                                     self.pad_upper_x,
                                                                                     self.pad_lower_x,
                                                                                     self.bounds_x)
            self.bounds_y, self.pad_upper_y, self.pad_lower_y = bounds(self.y,
                                                                                     self.bound_upper_y,
                                                                                     self.bound_lower_y,
                                                                                     self.pad_upper_y,
                                                                                     self.pad_lower_y,
                                                                                     self.bounds_y)
            self.bounds_z, self.pad_upper_z, self.pad_lower_z = bounds(self.z,
                                                                                     self.bound_upper_z,
                                                                                     self.bound_lower_z,
                                                                                     self.pad_upper_z,
                                                                                     self.pad_lower_z,
                                                                                     self.bounds_z)

            if self.pad_demo is True:
                pad_x = 0.05 * span(self.bounds_x)
                self.pad_upper_x = pad_x
                self.pad_lower_x = pad_x
                pad_y = 0.05 * span(self.bounds_y)
                self.pad_upper_y = pad_y
                self.pad_lower_y = pad_y
                pad_z = 0.05 * span(self.bounds_z)
                self.pad_upper_z = pad_z
                self.pad_lower_z = pad_z

            # Set bounds ignoring warnings if bounds are equal
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.ax.set_xlim3d(self.bounds_x[0] - self.pad_lower_x,
                                   self.bounds_x[1] + self.pad_upper_x)
                self.ax.set_ylim3d(self.bounds_y[0] - self.pad_lower_y,
                                   self.bounds_y[1] + self.pad_upper_y)
                self.ax.set_zlim3d(self.bounds_z[0] - self.pad_lower_y,
                                   self.bounds_z[1] + self.pad_upper_y)

    def method_scale(self):

        if all([ascale_x is not None for ascale_x in [self.scale_x, self.scale_y, self.scale_z]]):
            # Scaling
            mascale_x = max([self.scale_x, self.scale_y, self.scale_z])
            scale_x = self.scale_x/mascale_x
            scale_y = self.scale_y/mascale_x
            scale_z = self.scale_z/mascale_x

            scale_matrix = np.diag([scale_x, scale_y, scale_z, 1])

            # Reference:
            # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
            self.ax.get_proj = lambda: np.dot(Axes3D.get_proj(self.ax), scale_matrix)

        elif self.aspect_equal:
            # Aspect ratio of 1
            #
            # Due to the flawed Matplotlib 3D axis aspect ratio
            # implementation, the z axis will be shrunk if it is
            # the one with the highest span.
            # This a completely empirical conclusion based on
            # some testing, and so is the solution.
            # Reference: https://github.com/matplotlib/matplotlib/issues/1077/

            Z_CORRECTION_FACTOR = 1.4

            span_x = span(self.bounds_x)
            span_y = span(self.bounds_y)
            span_z = span(self.bounds_z)*Z_CORRECTION_FACTOR

            ranges = np.array([span_x,
                               span_y,
                               span_z])
            max_range = ranges.max()
            min_range = ranges[ranges > 0].min()

            scale_x = max(span_x, min_range)/max_range
            scale_y = max(span_y, min_range)/max_range
            scale_z = max(span_z, min_range)/max_range

            scale_matrix = np.diag([scale_x, scale_y, scale_z, 1])

            # Reference:
            # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
            self.ax.get_proj = lambda: np.dot(Axes3D.get_proj(self.ax), scale_matrix)

