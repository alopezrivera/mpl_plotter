import inspect
import difflib
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


class attributes:

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

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size+self.font_size_increase)
            self.legend = self.fig.legend(loc=self.legend_loc, prop=legend_font,
                                          handleheight=self.legend_handleheight, ncol=self.legend_ncol)

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
                    v = [self.x_lower_bound, self.x_upper_bound]
                if v[0] is None:
                    v[0] = l
                if v[1] is None:
                    v[1] = u
                return v, up, lp

            self.x_bounds, self.x_upper_resize_pad, self.x_lower_resize_pad = bounds(self.x,
                                                                                     self.x_upper_bound,
                                                                                     self.x_lower_bound,
                                                                                     self.x_upper_resize_pad,
                                                                                     self.x_lower_resize_pad,
                                                                                     self.x_bounds)
            self.y_bounds, self.y_upper_resize_pad, self.y_lower_resize_pad = bounds(self.y,
                                                                                     self.y_upper_bound,
                                                                                     self.y_lower_bound,
                                                                                     self.y_upper_resize_pad,
                                                                                     self.y_lower_resize_pad,
                                                                                     self.y_bounds)
            self.z_bounds, self.z_upper_resize_pad, self.z_lower_resize_pad = bounds(self.z,
                                                                                     self.z_upper_bound,
                                                                                     self.z_lower_bound,
                                                                                     self.z_upper_resize_pad,
                                                                                     self.z_lower_resize_pad,
                                                                                     self.z_bounds)

            if self.demo_pad_plot is True:
                pad_x = 0.05 * span(self.x_bounds)
                self.x_upper_resize_pad = pad_x
                self.x_lower_resize_pad = pad_x
                pad_y = 0.05 * span(self.y_bounds)
                self.y_upper_resize_pad = pad_y
                self.y_lower_resize_pad = pad_y
                pad_z = 0.05 * span(self.z_bounds)
                self.z_upper_resize_pad = pad_z
                self.z_lower_resize_pad = pad_z

            self.ax.set_xlim3d(self.x_bounds[0] - self.x_lower_resize_pad,
                               self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ylim3d(self.y_bounds[0] - self.y_lower_resize_pad,
                               self.y_bounds[1] + self.y_upper_resize_pad)
            self.ax.set_zlim3d(self.z_bounds[0] - self.y_lower_resize_pad,
                               self.z_bounds[1] + self.y_upper_resize_pad)

    def method_title(self):
        if self.title is not None:

            self.ax.set_title(self.title, y=self.title_y,
                              fontname=self.font if self.title_font is None else self.title_font,
                              weight=self.title_weight,
                              color=self.workspace_color if self.title_color is None else self.title_color,
                              size=self.title_size+self.font_size_increase)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if self.x_label is not None:
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=self.x_label_weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.x_label_size+self.font_size_increase, labelpad=self.x_label_pad,
                               rotation=self.x_label_rotation)

        if self.y_label is not None:
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=self.y_label_weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.y_label_size+self.font_size_increase, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)

        if self.z_label is not None:
            self.ax.set_zlabel(self.z_label, fontname=self.font, weight=self.z_label_weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.z_label_size+self.font_size_increase, labelpad=self.z_label_pad,
                               rotation=self.z_label_rotation)

    def method_spines(self):

        if self.spines_juggled is not None:
            self.ax.xaxis._axinfo['juggled'] = self.spines_juggled
        else:
            self.ax.xaxis._axinfo['juggled'] = (1, 0, 2)

    def method_ticks(self):
        # Tick number
        if self.x_tick_number is not None:
            # Tick locations
            if not(self.x_custom_tick_locations is None):
                low = self.x_custom_tick_locations[0]
                high = self.x_custom_tick_locations[1]
            else:
                low = self.x.min()
                high = self.x.max()
            # Set usual ticks
            if self.x_tick_number > 1 and span(self.x) != 0:
                ticklocs = np.linspace(low, high, self.x_tick_number)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_xticks(ticklocs)
        if self.y_tick_number is not None:
            # Tick locations
            if not (self.y_custom_tick_locations is None):
                low = self.y_custom_tick_locations[0]
                high = self.y_custom_tick_locations[1]
            else:
                low = self.y.min()
                high = self.y.max()
            # Set usual ticks
            if self.y_tick_number > 1 and span(self.y) != 0:
                ticklocs = np.linspace(low, high, self.y_tick_number)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low) / 2])
            self.ax.set_yticks(ticklocs)
        if self.z_tick_number is not None:
            # Tick locations
            if not (self.z_custom_tick_locations is None):
                low = self.z_custom_tick_locations[0]
                high = self.z_custom_tick_locations[1]
            else:
                low = self.z.min()
                high = self.z.max()
            # Set usual ticks
            if self.z_tick_number > 1 and span(self.z) != 0:
                ticklocs = np.linspace(low, high, self.z_tick_number)
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
        if self.x_custom_tick_labels is not None:
            self.ax.set_xticklabels(self.x_custom_tick_labels)
        if self.y_custom_tick_labels is not None:
            self.ax.set_yticklabels(self.y_custom_tick_labels)
        if self.z_custom_tick_labels is not None:
            self.ax.set_zticklabels(self.z_custom_tick_labels)
        # Label font, color, size, rotation
        for label in self.ax.get_xticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.x_tick_label_size is not None:
                label.set_fontsize(self.x_tick_label_size+self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.x_tick_rotation)
        for label in self.ax.get_yticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.y_tick_label_size is not None:
                label.set_fontsize(self.y_tick_label_size + self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.y_tick_rotation)
        for label in self.ax.get_zticklabels():
            label.set_fontname(self.font)
            label.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
            if self.z_tick_label_size is not None:
                label.set_fontsize(self.z_tick_label_size + self.font_size_increase)
            else:
                label.set_fontsize(self.tick_label_size + self.font_size_increase)
            label.set_rotation(self.z_tick_rotation)
        # Label float format
        float_format = lambda x: '%.' + str(x) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format(self.x_tick_ndecimals)))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format(self.y_tick_ndecimals)))
        self.ax.zaxis.set_major_formatter(FormatStrFormatter(float_format(self.z_tick_ndecimals)))
        # Label pad
        if self.x_tick_label_pad is not None:
            self.ax.tick_params(axis='x', pad=self.x_tick_label_pad)
        if self.y_tick_label_pad is not None:
            self.ax.tick_params(axis='y', pad=self.y_tick_label_pad)
        if self.z_tick_label_pad is not None:
            self.ax.tick_params(axis='z', pad=self.z_tick_label_pad)

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

        if all([ax_scale is not None for ax_scale in [self.x_scale, self.y_scale, self.z_scale]]):
            # Scaling
            max_scale = max([self.x_scale, self.y_scale, self.z_scale])
            x_scale = self.x_scale/max_scale
            y_scale = self.y_scale/max_scale
            z_scale = self.z_scale/max_scale

            scale_matrix = np.diag([x_scale, y_scale, z_scale, 1])

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

            span_x = span(self.x_bounds)
            span_y = span(self.y_bounds)
            span_z = span(self.z_bounds)*Z_CORRECTION_FACTOR

            ranges = np.array([span_x,
                               span_y,
                               span_z])
            max_range = ranges.max()
            min_range = ranges[ranges > 0].min()

            x_scale = max(span_x, min_range)/max_range
            y_scale = max(span_y, min_range)/max_range
            z_scale = max(span_z, min_range)/max_range

            scale_matrix = np.diag([x_scale, y_scale, z_scale, 1])

            # Reference:
            # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
            self.ax.get_proj = lambda: np.dot(Axes3D.get_proj(self.ax), scale_matrix)


class plot(canvas, attributes):

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

        # Save
        self.method_save()

        self.method_show()

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.show is True:
            self.fig.tight_layout()
            self.plt.show()
        else:
            if self.suppress is False:
                print('Ready for next subplot')


class color:

    def method_cb(self):
        if self.color_bar is True:
            if self.norm is None:
                return print_color("No norm selected for colorbar. Set norm=<parameter of choice>", "grey")

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
                                     ticks=locator, boundaries=locator if self.cb_hard_bounds is True else None,
                                     spacing='proportional',
                                     extend=self.extend,
                                     format='%.' + str(self.cb_tick_ndecimals) + 'f',
                                     pad=self.cb_pad,
                                     )

            # Ticks
            #   Locator
            cbar.locator = locator
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Title
            if self.cb_orientation == 'vertical':
                if self.cb_title is not None and self.cb_y_title is False and self.cb_top_title is False:
                    print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
                if self.cb_y_title is True:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_ytitle_labelpad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size+self.font_size_increase,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                if self.cb_top_title is True:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_top_title_pad)
                    cbar.ax.title.set_position((self.x_cb_top_title, self.cb_top_title_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title_size+self.font_size_increase)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size+self.font_size_increase,
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
            if self.cmap_lighting is None:
                try:
                    cmap = difflib.get_close_matches(self.color, self.plt.colormaps())[0]
                    print_color(
                        f'You have selected the solid _color_ "{self.color}" for your surface, and set _lighting_ as True\n\n'
                        f'   The search for Matplotlib colormaps similar to "{self.color}" has resulted in: \n',
                        "blue")
                    print(f'       "{cmap}"\n')
                    print_color(
                        '   Specify a custom colormap for the lighting function with the _cmap_lighting_ attribute.\n'
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
                        '   Specify a custom colormap for the lighting function with the _cmap_lighting_ attribute.\n'
                        '   NOTE: This will overrule your monochrome color, however. Set _lighting_ to False if this is undesired.',
                        "red")
            else:
                cmap = self.cmap_lighting
        else:
            cmap = self.cmap_lighting if self.cmap_lighting is not None else self.cmap

        rgb = ls.shade(self.z,
                       cmap=cm.get_cmap(cmap),
                       vert_exag=0.1, blend_mode='soft')

        return rgb

    def method_edges_to_rgba(self):
        if self.edges_to_rgba is True:
            self.graph.set_edgecolors(self.graph.to_rgba(self.graph._A))


class line(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, line_width=5,
                 # Specifics: color
                 color='darkred', cmap='RdBu_r', alpha=1,
                 # Scale
                 x_scale=None,
                 y_scale=None,
                 z_scale=None,
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
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 z_upper_bound=None, z_lower_bound=None,
                 x_bounds=None, y_bounds=None, z_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 z_upper_resize_pad=0, z_lower_resize_pad=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_weight='normal', x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_weight='normal', y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_weight='normal', z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None, x_custom_tick_labels=None, x_custom_tick_locations=None,
                 y_tick_number=5, y_tick_labels=None, y_custom_tick_labels=None, y_custom_tick_locations=None,
                 z_tick_number=5, z_tick_labels=None, z_custom_tick_labels=None, z_custom_tick_locations=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None,
                 x_tick_label_pad=4,
                 y_tick_label_pad=4,
                 z_tick_label_pad=4,
                 x_tick_ndecimals=1,
                 y_tick_ndecimals=1,
                 z_tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None, z_tick_label_size=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, newplot=False,
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
        "param norm: Norm to assign colormap values

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

        self.graph = self.ax.plot3D(self.x, self.y, self.z, alpha=self.alpha, linewidth=self.line_width,
                                    color=self.color, label=self.plot_label)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 1000)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)


class scatter(plot, color):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, point_size=30, marker="o",
                 # Specifics: color
                 alpha=1,
                 color='darkred',
                 cmap='RdBu_r', color_rule=None,
                 # Color bar
                 color_bar=False, cb_pad=0.1, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10,
                 cb_tick_number=5, cb_tick_ndecimals=5,
                 shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Scale
                 x_scale=None,
                 y_scale=None,
                 z_scale=None,
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
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 z_upper_bound=None, z_lower_bound=None,
                 x_bounds=None, y_bounds=None, z_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 z_upper_resize_pad=0, z_lower_resize_pad=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_weight='normal', x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_weight='normal', y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_weight='normal', z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None, x_custom_tick_labels=None, x_custom_tick_locations=None,
                 y_tick_number=5, y_tick_labels=None, y_custom_tick_labels=None, y_custom_tick_locations=None,
                 z_tick_number=5, z_tick_labels=None, z_custom_tick_labels=None, z_custom_tick_locations=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None,
                 x_tick_label_pad=4,
                 y_tick_label_pad=4,
                 z_tick_label_pad=4,
                 x_tick_ndecimals=1,
                 y_tick_ndecimals=1,
                 z_tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None, z_tick_label_size=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, newplot=False,
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
        :param point_size: Point size
        :param marker: Dot marker

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        "param norm: Norm to assign colormap values

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
                                         s=self.point_size, marker=self.marker,
                                         c=self.color_rule, cmap=self.cmap,
                                         alpha=self.alpha)
            self.method_cb()
        else:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.point_size, marker=self.marker,
                                         color=self.color,
                                         alpha=self.alpha)

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x = np.linspace(-2, 2, 20)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)
            self.color_rule = self.z


class surface(plot, surf):

    def __init__(self,
                 # Specifics: surface
                 x=None, y=None, z=None, rstride=1, cstride=1, line_width=0.1,
                 # Specifics: lighting
                 lighting=False, antialiased=False, shade=False,
                 # Specifics: color
                 cmap='RdBu_r', cmap_lighting=None,
                 color_rule=None, norm=None,
                 color=None,
                 # Color bar
                 color_bar=False, cb_pad=0.1, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10,
                 cb_tick_number=5, cb_tick_ndecimals=5,
                 shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 alpha=1, edge_color='black', edges_to_rgba=False,
                 # Scale
                 x_scale=None,
                 y_scale=None,
                 z_scale=None,
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
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 z_upper_bound=None, z_lower_bound=None,
                 x_bounds=None, y_bounds=None, z_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 z_upper_resize_pad=0, z_lower_resize_pad=0,
                 # Axes
                 show_axes=True,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_weight='normal', title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_weight='normal', x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_weight='normal', y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_weight='normal', z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None, x_custom_tick_labels=None, x_custom_tick_locations=None,
                 y_tick_number=5, y_tick_labels=None, y_custom_tick_labels=None, y_custom_tick_locations=None,
                 z_tick_number=5, z_tick_labels=None, z_custom_tick_labels=None, z_custom_tick_locations=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None,
                 x_tick_label_pad=4,
                 y_tick_label_pad=4,
                 z_tick_label_pad=4,
                 x_tick_ndecimals=1,
                 y_tick_ndecimals=1,
                 z_tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None, z_tick_label_size=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, newplot=False,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Surface class
        mpl_plotter - 3D

        Important combinations:
            Wireframe: alpha=0, line_width>0, edges_to_rgba=False

        Specifics

        - Surface
        :param x: x
        :param y: y
        :param z: z
        :param rstride: Surface grid definition
        :param cstride: Surface grid definition
        :param line_width: Width of interpolating lines

        - Lighting
        :param lighting: Apply lighting
        :param antialiased: Apply antialiasing
        :param shade: Apply shading

        - Color
        :param norm: Instance of matplotlib.colors.Normalize.
            norm = matplotlib.colors.Normalize(vmin=<vmin>, vmax=<vmax>)
        :param edge_color: Color of surface plot edges
        :param edges_to_rgba: Remove lines from surface plot
        :param alpha: Transparency
        :param cmap: Colormap
        :param cmap_lighting: Colormap used for lighting

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
        if self.lighting:
            # Lightning
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.alpha,
                                              cmap=self.cmap if self.color is None else None,
                                              norm=self.norm, color=self.color,
                                              edgecolors=self.edge_color,
                                              facecolors=self.method_lighting(),
                                              rstride=self.rstride, cstride=self.cstride, linewidth=self.line_width,
                                              antialiased=self.antialiased, shade=self.shade,
                                              )
        elif self.color_rule is not None:
            # Colormap
            cmap = mpl.cm.get_cmap(self.cmap) if not isinstance(self.cmap, mpl.colors.LinearSegmentedColormap) else self.cmap
            facecolors = cmap((self.color_rule+abs(self.color_rule.min()))/(self.color_rule.max()+abs(self.color_rule.min())))

            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.alpha,
                                              cmap=self.cmap,
                                              norm=self.norm,
                                              facecolors=facecolors,
                                              edgecolors=self.edge_color,
                                              rstride=self.rstride, cstride=self.cstride, linewidth=self.line_width,
                                              antialiased=self.antialiased, shade=self.shade,
                                              )
        elif self.norm is not None:
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.alpha,
                                              cmap=self.cmap,
                                              norm=self.norm,
                                              edgecolors=self.edge_color,
                                              rstride=self.rstride, cstride=self.cstride, linewidth=self.line_width,
                                              antialiased=self.antialiased, shade=self.shade,
                                              )
        else:
            # No colormap
            self.graph = self.ax.plot_surface(self.x, self.y, self.z,
                                              alpha=self.alpha,
                                              color=self.color,
                                              edgecolors=self.edge_color,
                                              rstride=self.rstride, cstride=self.cstride, linewidth=self.line_width,
                                              antialiased=self.antialiased, shade=self.shade,
                                              )

    def mock(self):
        if self.x is None and self.y is None and self.z is None:
            self.x, self.y, self.z = MockData().hill()
            self.norm = mpl.colors.Normalize(vmin=self.z.min(), vmax=self.z.max())


def floating_text(ax, text, font, x, y, z, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, z, text, size=size, weight=weight, fontdict=font)
