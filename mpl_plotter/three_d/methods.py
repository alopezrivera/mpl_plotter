# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Plotting Methods
----------------
"""

import inspect
import difflib
import warnings
import numpy as np
import matplotlib as mpl

from matplotlib import font_manager
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

from importlib import import_module

from alexandria.shell import print_color
from alexandria.data_structs.array import span, ensure_ndarray

from mpl_plotter import figure
from mpl_plotter.three_d.mock import MockData


class canvas:

    def method_backend(self):
        if self.backend is not None:
            try:
                mpl.use(self.backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(self.backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

    def method_fonts(self):
        """
        Fonts
        Reference:
            - https://matplotlib.org/2.0.2/users/customizing.html
        Pyplot method:
            plt.rcParams['<category>.<item>'] = <>
        """
        mpl.rc('font', family=self.font)
        mpl.rc('font', serif="DejaVu Serif" if self.font == "serif" else self.font)
        self.plt.rcParams['font.sans-serif'] ="DejaVu Serif" if self.font == "serif" else self.font
        mpl.rc('font', cursive="Apple Chancery" if self.font == "serif" else self.font)
        mpl.rc('font', fantasy="Chicago" if self.font == "serif" else self.font)
        mpl.rc('font', monospace="Bitstream Vera Sans Mono" if self.font == "serif" else self.font)

        mpl.rc('mathtext', fontset=self.math_font)

        mpl.rc('text', color=self.font_color)
        mpl.rc('xtick', color=self.font_color)
        mpl.rc('ytick', color=self.font_color)
        mpl.rc('axes', labelcolor=self.font_color)

    def method_figure(self):
        if self.style is not None:
            self.plt.style.use(self.style)
        self.fig = figure(figsize=self.figsize)

    def method_setup(self):
        if self.fig is None:
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                axes = self.fig.axes
                for ax in axes:
                    if ax.__class__.__name__ == 'Axes3DSubplot':
                        self.ax = ax

        if self.ax is None:
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box', projection='3d')

        self.ax.view_init(azim=self.azim, elev=self.elev)

    def method_grid(self):
        if self.grid:
            self.plt.grid(linestyle=self.grid_lines, color=self.grid_color)
        else:
            self.ax.grid(self.grid)
        if not self.show_axes:
            self.plt.axis('off')

    def method_pane_fill(self):
        # Pane fill - False by default
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        # Pane color - transparent by default
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        if self.pane_fill is not None:
            # Set pane fill to True if a color is provided
            self.ax.xaxis.pane.fill = True if self.pane_fill is not None else False
            self.ax.yaxis.pane.fill = True if self.pane_fill is not None else False
            self.ax.zaxis.pane.fill = True if self.pane_fill is not None else False
            # Set pane fill color to that specified
            self.ax.xaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))
            self.ax.yaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))
            self.ax.zaxis.set_pane_color(mpl.colors.to_rgba(self.pane_fill))

        # Set edge colors
        if self.blend_edges:
            if self.pane_fill is not None:
                spine_color = self.pane_fill
            else:
                spine_color = (0, 0, 0, 0)
        else:
            spine_color = self.spine_color

        self.ax.xaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "x")
                                         else self.background_color_plot)
        self.ax.yaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "y")
                                         else self.background_color_plot)
        self.ax.zaxis.pane.set_edgecolor(spine_color if np.any(np.array(self.remove_axis).flatten() == "z")
                                         else self.background_color_plot)

    def method_background_color(self):
        self.fig.patch.set_facecolor(self.background_color_figure)
        self.ax.set_facecolor(self.background_color_plot)
        self.ax.patch.set_alpha(self.background_alpha)

    def method_workspace_style(self):
        if self.light:
            self.workspace_color = 'black' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if self.workspace_color is None else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if self.workspace_color2 is None else self.workspace_color2
            self.style = None


class attributes:

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size+self.font_size_increase)
            self.legend = self.fig.legend(loc=self.legend_loc, prop=legend_font,
                                          handleheight=self.legend_handleheight, ncol=self.legend_columns)

    def method_title(self):
        if self.title is not None:

            self.ax.set_title(self.title,
                              y=self.title_y,
                              fontname=self.font if self.title_font is None else self.title_font,
                              weight=self.title_weight,
                              color=self.workspace_color if self.title_color is None else self.title_color,
                              size=self.title_size+self.font_size_increase)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if self.label_x is not None:
            self.ax.set_xlabel(self.label_x, fontname=self.font, weight=self.label_weight_x,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_x+self.font_size_increase, labelpad=self.label_pad_x,
                               rotation=self.label_rotation_x)

        if self.label_y is not None:
            self.ax.set_ylabel(self.label_y, fontname=self.font, weight=self.label_weight_y,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_y+self.font_size_increase, labelpad=self.label_pad_y,
                               rotation=self.label_rotation_y)

        if self.label_z is not None:
            self.ax.set_zlabel(self.label_z, fontname=self.font, weight=self.label_weight_z,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.label_size_z+self.font_size_increase, labelpad=self.label_pad_z,
                               rotation=self.label_rotation_z)

    def method_spines(self):

        if self.spines_juggled is not None:
            self.ax.xaxis._axinfo['juggled'] = self.spines_juggled
        else:
            self.ax.xaxis._axinfo['juggled'] = (1, 0, 2)

    def method_ticks(self):
        # Tick number
        if self.tick_number_x is not None:
            # Tick locations
            if not(self.tick_locations_x is None):
                low = self.tick_locations_x[0]
                high = self.tick_locations_x[1]
            else:
                low = self.x.min()
                high = self.x.max()
            # Set usual ticks
            if self.tick_number_x > 1 and span(self.x) != 0:
                ticklocs = np.linspace(low, high, self.tick_number_x)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_xticks(ticklocs)
        if self.tick_number_y is not None:
            # Tick locations
            if not (self.tick_locations_y is None):
                low = self.tick_locations_y[0]
                high = self.tick_locations_y[1]
            else:
                low = self.y.min()
                high = self.y.max()
            # Set usual ticks
            if self.tick_number_y > 1 and span(self.y) != 0:
                ticklocs = np.linspace(low, high, self.tick_number_y)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low) / 2])
            self.ax.set_yticks(ticklocs)
        if self.tick_number_z is not None:
            # Tick locations
            if not (self.tick_locations_z is None):
                low = self.tick_locations_z[0]
                high = self.tick_locations_z[1]
            else:
                low = self.z.min()
                high = self.z.max()
            # Set usual ticks
            if self.tick_number_z > 1 and span(self.z) != 0:
                ticklocs = np.linspace(low, high, self.tick_number_z)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low) / 2])
            self.ax.set_zticks(ticklocs)
        # Tick color
        if self.tick_color is not None:
            self.ax.tick_params(axis='both', color=self.tick_color)
            self.ax.xaxis.line.set_color(
                self.spine_color if self.spine_color is not None else self.workspace_color)
            self.ax.yaxis.line.set_color(
                self.spine_color if self.spine_color is not None else self.workspace_color)
            self.ax.zaxis.line.set_color(
                self.spine_color if self.spine_color is not None else self.workspace_color)
        # Custom tick labels
        if self.tick_labels_x is not None:
            self.ax.set_xticklabels(self.tick_labels_x)
        if self.tick_labels_y is not None:
            self.ax.set_yticklabels(self.tick_labels_y)
        if self.tick_labels_z is not None:
            self.ax.set_zticklabels(self.tick_labels_z)
        # Label font, color, size, rotation
        for label in self.ax.get_xticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.tick_label_size_x is not None:
                label.set_fontsize(self.tick_label_size_x+self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.tick_rotation_x)
        for label in self.ax.get_yticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.tick_label_size_y is not None:
                label.set_fontsize(self.tick_label_size_y + self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.tick_rotation_y)
        for label in self.ax.get_zticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.tick_label_size_z is not None:
                label.set_fontsize(self.tick_label_size_z + self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.tick_rotation_z)
        # Label float format
        float_format = lambda x: '%.' + str(x) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format(self.tick_label_decimals_x if self.tick_label_decimals_x is not None else self.tick_label_decimals)))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format(self.tick_label_decimals_y if self.tick_label_decimals_y is not None else self.tick_label_decimals)))
        self.ax.zaxis.set_major_formatter(FormatStrFormatter(float_format(self.tick_label_decimals_z if self.tick_label_decimals_z is not None else self.tick_label_decimals)))
        # Label pad
        if self.tick_label_pad_x is not None:
            self.ax.tick_params(axis='x', pad=self.tick_label_pad_x)
        if self.tick_label_pad_y is not None:
            self.ax.tick_params(axis='y', pad=self.tick_label_pad_y)
        if self.tick_label_pad_z is not None:
            self.ax.tick_params(axis='z', pad=self.tick_label_pad_z)


class adjustments:

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

    def method_subplots_adjust(self):

        self.plt.subplots_adjust(
            top    = self.top,
            bottom = self.bottom,
            left   = self.left,
            right  = self.right,
            hspace = self.hspace,
            wspace = self.wspace)

    def method_remove_axes(self):
        if self.remove_axis is not None:
            for axis in np.array(self.remove_axis).flatten():
                if axis == "x":
                    self.ax.xaxis.line.set_lw(0.)
                    self.ax.set_xticks([])
                if axis == "y":
                    self.ax.yaxis.line.set_lw(0.)
                    self.ax.set_yticks([])
                if axis == "z":
                    self.ax.zaxis.line.set_lw(0.)
                    self.ax.set_zticks([])

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


class plot(canvas, attributes, adjustments):

    def init(self):

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def run(self):
        self.main()
        try:
            self.custom()
        except AttributeError:
            pass
        self.finish()

    def main(self):
        # Canvas setup
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_pane_fill()
        self.method_background_color()
        self.method_workspace_style()

        # Mock plot
        self.mock()
        # Plot
        self.plot()

    def finish(self):
        # Scale and axis resizing
        self.method_resize_axes()
        self.method_scale()

        # Legend
        self.method_legend()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_remove_axes()

        # Adjust
        self.method_subplots_adjust()

        # Save
        self.method_save()

        self.method_show()

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.show is True:
            self.plt.show()
        else:
            if self.suppress is False:
                print('Ready for next subplot')


class color:

    def method_cb(self):
        if self.color_bar is True:
            if self.color_rule is None:
                return print_color("No surface_norm selected for colorbar. Set surface_norm=<parameter of choice>", "grey")

            # Obtain and apply limits
            if self.cb_vmin is None:
                self.cb_vmin = self.color_rule.min()
            if self.cb_vmax is None:
                self.cb_vmax = self.color_rule.max()
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_tick_number)

            # Colorbar
            cbar = self.fig.colorbar(self.graph,
                                     ax=self.ax,
                                     orientation=self.cb_orientation, shrink=self.shrink,
                                     ticks=locator, boundaries=locator if self.cb_bounds_hard is True else None,
                                     spacing='proportional',
                                     extend=self.extend,
                                     format='%.' + str(self.cb_tick_label_decimals) + 'f',
                                     pad=self.cb_pad,
                                     )

            # Ticks
            #   Locator
            cbar.locator = locator
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.ctick_label_pad_b, labelsize=self.ctick_label_size_b)

            # Title
            if self.cb_orientation == 'vertical':
                if self.cb_title is not None and self.cb_title_y is False and self.cb_title_top is False:
                    print('Input colorbar title location with booleans: cb_title_y=True or cb_title_top=True')
                if self.cb_title_y is True:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_title_pad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size + self.font_size_increase,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                if self.cb_title_top is True:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_title_pad)
                    cbar.ax.title.set_position((self.cb_title_top_pos_x, self.cb_title_top_pos_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title_size + self.font_size_increase)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_title_pad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size + self.font_size_increase,
                                                       weight=self.cb_title_weight)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)


class surf(color):

    def custom(self):
        self.method_cb()
        self.method_edges_to_rgba()

    def method_lighting(self):
        ls = LightSource(270, 45)

        if self.color is not None:
            if self.surface_cmap_lighting is None:
                try:
                    cmap = difflib.get_close_matches(self.color, self.plt.colormaps())[0]
                    print_color(
                        f'You have selected the solid _color_ "{self.color}" for your surface, and set _lighting_ as True\n\n'
                        f'   The search for Matplotlib colormaps similar to "{self.color}" has resulted in: \n',
                        "blue")
                    print(f'       "{cmap}"\n')
                    print_color(
                        '   Specify a custom colormap for the lighting function with the _surface_cmap_lighting_ attribute.\n'
                        '   NOTE: This will overrule your monochrome color, however. Set _lighting_ to False if this is undesired.',
                        "blue")
                except IndexError:
                    cmap = "Greys"
                    print_color(
                        f'You have selected the solid _color_ "{self.color}" for your surface, and set _lighting_ as True\n\n'
                        f'   The search for Matplotlib colormaps similar to "{self.color}" has failed. Reverting to\n',
                        "red")
                    print(f'       "{cmap}"\n')
                    print_color(
                        '   Specify a custom colormap for the lighting function with the _surface_cmap_lighting_ attribute.\n'
                        '   NOTE: This will overrule your monochrome color, however. Set _lighting_ to False if this is undesired.',
                        "red")
            else:
                cmap = self.surface_cmap_lighting
        else:
            cmap = self.surface_cmap_lighting if self.surface_cmap_lighting is not None else self.cmap

        rgb = ls.surface_shade(self.z,
                       cmap=cm.get_cmap(cmap),
                       vert_exag=0.1, blend_mode='soft')

        return rgb

    def method_edges_to_rgba(self):
        if self.surface_edges_to_rgba is True:
            self.graph.set_edgecolors(self.graph.to_rgba(self.graph._A))


class line(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, line_width=5, line_alpha=1,
                 # Specifics: color
                 color='darkred', cmap='RdBu_r',
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_locations_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_locations_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_locations_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Line class
        mpl_plotter - 3D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param line_width: Line width

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        "param surface_norm: Norm to assign colormap values

        Other
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(line).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):

        self.graph = self.ax.plot3D(self.x, self.y, self.z, alpha=self.line_alpha, linewidth=self.line_width,
                                    color=self.color, label=self.plot_label)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 1000)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)


class scatter(plot, color):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, scatter_size=30, scatter_marker="o", 
                 scatter_facecolors=None, color_rule=None, scatter_alpha=1,
                 # Color
                 color='darkred', cmap='RdBu_r',
                 # Color bar
                 color_bar=False, cb_orientation='vertical', shrink=0.75,
                 extend='neither', cb_vmin=None, cb_vmax=None, cb_bounds_hard=False,
                 cb_pad=0.1, cb_outline_width=None,                 
                 cb_tick_number=5, cb_tick_label_decimals=5, ctick_label_size_b=10, ctick_label_pad_b=10,
                 cb_title=None, cb_title_top=True, cb_title_y=False,
                 cb_title_top_pos_x=0, cb_title_top_pos_y=1,
                 cb_title_pad=10, cb_title_weight='normal',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_locations_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_locations_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_locations_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Scatter class
        mpl_plotter - 3D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param scatter_size: Point size
        :param scatter_marker: Dot scatter_marker

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        "param surface_norm: Norm to assign colormap values

        Other
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(scatter).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):

        if self.color_rule is not None:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.scatter_size, marker=self.scatter_marker, facecolors=self.scatter_facecolors,
                                         c=self.color_rule, cmap=self.cmap,
                                         alpha=self.scatter_alpha)
            self.method_cb()
        else:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.scatter_size, marker=self.scatter_marker, facecolors=self.scatter_facecolors,
                                         color=self.color,
                                         alpha=self.scatter_alpha)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 20)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)
            self.color_rule = self.z


class surface(plot, surf):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, surface_rstride=1, surface_cstride=1, surface_wire_width=0.1,
                 surface_lighting=False, surface_antialiased=False, surface_shade=False, surface_alpha=1,
                 surface_cmap_lighting=None, surface_norm=None,
                 surface_edge_color='black', surface_edges_to_rgba=False,
                 # Specifics: color
                 cmap='RdBu_r', color=None, color_rule=None,
                 # Color bar
                 color_bar=False, cb_orientation='vertical', shrink=0.75,
                 extend='neither', cb_vmin=None, cb_vmax=None, cb_bounds_hard=False,
                 cb_pad=0.1, cb_outline_width=None,                 
                 cb_tick_number=5, cb_tick_label_decimals=5, ctick_label_size_b=10, ctick_label_pad_b=10,
                 cb_title=None, cb_title_top=True, cb_title_y=False,
                 cb_title_top_pos_x=0, cb_title_top_pos_y=1,
                 cb_title_pad=10, cb_title_weight='normal',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 # Scale
                 scale_x=None,
                 scale_y=None,
                 scale_z=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axis
                 fig=None, ax=None, figsize=(5, 4), shape_and_position=111, azim=-138, elev=19, remove_axis=None,
                 # Setup
                 prune=None, resize_axes=True, aspect_equal=False, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None, blend_edges=False,
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 pane_fill=None,
                 # Bounds
                 bound_upper_x=None, bound_lower_x=None,
                 bound_upper_y=None, bound_lower_y=None,
                 bound_upper_z=None, bound_lower_z=None,
                 bounds_x=None, bounds_y=None, bounds_z=None,
                 # Pads
                 pad_demo=False,
                 pad_upper_x=0, pad_lower_x=0,
                 pad_upper_y=0, pad_lower_y=0,
                 pad_upper_z=0, pad_lower_z=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 label_x='x', label_weight_x='normal', label_size_x=12, label_pad_x=7, label_rotation_x=None,
                 label_y='y', label_weight_y='normal', label_size_y=12, label_pad_y=7, label_rotation_y=None,
                 label_z='z', label_weight_z='normal', label_size_z=12, label_pad_z=7, label_rotation_z=None,
                 # Ticks
                 tick_color=None,
                 tick_number_x=5, tick_labels_x=None, tick_locations_x=None, tick_rotation_x=None,
                 tick_number_y=5, tick_labels_y=None, tick_locations_y=None, tick_rotation_y=None,
                 tick_number_z=5, tick_labels_z=None, tick_locations_z=None, tick_rotation_z=None,
                 # Tick labels
                 tick_label_size=10,
                 tick_label_decimals=1,
                 tick_label_pad_x=4, tick_label_decimals_x=None, tick_label_size_x=None,
                 tick_label_pad_y=4, tick_label_decimals_y=None, tick_label_size_y=None,
                 tick_label_pad_z=4, tick_label_decimals_z=None, tick_label_size_z=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_columns=1,
                 # Subplots
                 show=False,
                 top=0.975,
                 bottom=0.085,
                 left=0.14,
                 right=0.945,
                 hspace=0.2,
                 wspace=0.2,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Surface class
        mpl_plotter - 3D

        Important combinations:
            Wireframe: alpha=0, line_width>0, surface_edges_to_rgba=False

        Specifics

        - Surface
        :param x: x
        :param y: y
        :param z: z
        :param surface_rstride: Surface grid definition
        :param surface_cstride: Surface grid definition
        :param line_width: Width of interpolating lines

        - Lighting
        :param surface_lighting: Apply lighting
        :param surface_antialiased: Apply antialiasing
        :param surface_shade: Apply shading

        - Color
        :param surface_norm: Instance of matplotlib.colors.Normalize.
            surface_norm = matplotlib.colors.Normalize(vmin=<vmin>, vmax=<vmax>)
        :param surface_edge_color: Color of surface plot edges
        :param surface_edges_to_rgba: Remove lines from surface plot
        :param alpha: Transparency
        :param cmap: Colormap
        :param surface_cmap_lighting: Colormap used for lighting

        Other
        :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                        Backend error:
                            pip install pyqt5
                            pip install tkinter
                            pip install tk
                            ... stackoverflow
                        Plotting window freezes even if trying different backends with no backend error: python configuration problem
                            backend=None
        """

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(surface).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = ensure_ndarray(self.x) if self.x is not None else self.x
        self.y = ensure_ndarray(self.y) if self.y is not None else self.y
        self.z = ensure_ndarray(self.z) if self.z is not None else self.z

        self.init()

    def plot(self):
        if self.surface_lighting:
            # Lightning
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.surface_alpha,
                                              cmap=self.cmap if self.color is None else None,
                                              norm=self.surface_norm, color=self.color,
                                              edgecolors=self.surface_edge_color,
                                              facecolors=self.method_lighting(),
                                              rstride=self.surface_rstride, cstride=self.surface_cstride, linewidth=self.surface_wire_width,
                                              surface_antialiased=self.surface_antialiased, shade=self.surface_shade,
                                              )
        elif self.color_rule is not None:
            # Colormap
            cmap = mpl.cm.get_cmap(self.cmap) if not isinstance(self.cmap, mpl.colors.LinearSegmentedColormap) else self.cmap
            surface_facecolors = cmap((self.color_rule + abs(self.color_rule.min()))/(self.color_rule.max() + abs(self.color_rule.min())))

            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.surface_alpha,
                                              cmap=self.cmap,
                                              norm=self.surface_norm,
                                              facecolors=surface_facecolors,
                                              edgecolors=self.surface_edge_color,
                                              rstride=self.surface_rstride, cstride=self.surface_cstride, linewidth=self.surface_wire_width,
                                              antialiased=self.surface_antialiased, shade=self.surface_shade,
                                              )
        elif self.surface_norm is not None:
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.surface_alpha,
                                              cmap=self.cmap,
                                              norm=self.surface_norm,
                                              edgecolors=self.surface_edge_color,
                                              rstride=self.surface_rstride, cstride=self.surface_cstride, linewidth=self.surface_wire_width,
                                              antialiased=self.surface_antialiased, shade=self.surface_shade,
                                              )
        else:
            # No colormap
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.surface_alpha,
                                              color=self.color,
                                              edgecolors=self.surface_edge_color,
                                              rstride=self.surface_rstride, cstride=self.surface_cstride, linewidth=self.surface_wire_width,
                                              antialiased=self.surface_antialiased, shade=self.surface_shade,
                                              )

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x, self.y, self.z = MockData().hill()
            self.surface_norm = mpl.colors.Normalize(vmin=self.z.min(), vmax=self.z.max())


def floating_text(ax, text, font, x, y, z, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, z, text, size=size, weight=weight, fontdict=font)
