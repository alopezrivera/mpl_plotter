import inspect
import numpy as np
import matplotlib as mpl

from matplotlib import font_manager
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

from importlib import import_module

from mpl_plotter.methods.mock_data import MockData
from Alexandria.general.console import print_color


class canvas:

    def method_style(self):
        if self.light:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2,
                                                                                 type(None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = None

    def method_setup(self):
        if isinstance(self.fig, type(None)):
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                self.ax = self.plt.gca()

        if isinstance(self.ax, type(None)):
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box', projection='3d',
                                           facecolor=self.background_color_figure)

        self.ax.view_init(azim=self.azim, elev=self.elev)

    def method_figure(self):
        if not isinstance(self.style, type(None)):
            self.plt.style.use(self.style)
        self.fig = self.plt.figure(figsize=self.figsize)


class attributes:

    def method_background_color(self):
        self.ax.patch.set_alpha(self.background_alpha)

    def method_grid(self):
        if self.grid is not False:
            self.plt.grid(linestyle=self.grid_lines, color=self.grid_color)

    def method_pane_fill(self):
        # Pane fill and pane edge color
        self.ax.xaxis.pane.fill = self.pane_fill
        self.ax.yaxis.pane.fill = self.pane_fill
        self.ax.zaxis.pane.fill = self.pane_fill
        self.ax.xaxis.pane.set_edgecolor(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)
        self.ax.yaxis.pane.set_edgecolor(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            self.legend = self.fig.legend(loc=self.legend_loc, prop=legend_font,
                                          handleheight=self.legend_handleheight, ncol=self.legend_ncol)

    def method_title(self):
        if not isinstance(self.title, type(None)):

            self.ax.set_title(self.title, y=self.title_y,
                              fontname=self.font if isinstance(self.title_font, type(None)) else self.title_font,
                              weight=self.title_weight,
                              color=self.workspace_color if isinstance(self.title_color, type(None)) else self.title_color,
                              size=self.title_size)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if not isinstance(self.x_label, type(None)):
            if self.x_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.x_label_size, labelpad=self.x_label_pad,
                               rotation=self.x_label_rotation)
        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
        if not isinstance(self.z_label, type(None)):
            if self.z_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_zlabel(self.z_label, fontname=self.font, weight=weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.z_label_size, labelpad=self.z_label_pad,
                               rotation=self.z_label_rotation)

    def method_spines(self):

        for spine in self.ax.spines.values():
            spine.set_color(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)

        top = True
        right = True
        left = True
        bottom = True

        if not isinstance(self.spines_juggled, type(None)):
            self.ax.xaxis._axinfo['juggled'] = self.spines_juggled
        else:
            # self.ax.xaxis._axinfo['juggled'] = (0, 2, 1)
            # self.ax.xaxis._axinfo['juggled'] = (0, 1, 2)
            self.ax.xaxis._axinfo['juggled'] = (1, 0, 2)

        self.ax.tick_params(axis='both', which='both', top=top, right=right, left=left, bottom=bottom)

    def method_ticks(self):
        #   Color
        if self.tick_color is not None:
            self.ax.tick_params(axis='both', color=self.tick_color)

            self.ax.w_xaxis.line.set_color(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)
            self.ax.w_yaxis.line.set_color(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)
            self.ax.w_zaxis.line.set_color(self.spine_color if not isinstance(self.spine_color, type(None)) else self.workspace_color)

        #   Label size
        if self.tick_label_size is not None:
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Numeral size
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
        for tick in self.ax.get_zticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.zaxis.set_major_formatter(FormatStrFormatter(float_format))

        # Tick number
        if self.x_tick_number is not None:
            self.ax.xaxis.set_major_locator(self.plt.MaxNLocator(self.x_tick_number, prune=self.prune))
        if self.y_tick_number is not None:
            self.ax.yaxis.set_major_locator(self.plt.MaxNLocator(self.y_tick_number, prune=self.prune))
        if self.z_tick_number is not None:
            self.ax.zaxis.set_major_locator(self.plt.MaxNLocator(self.z_tick_number, prune=self.prune))

        # Tick label pad
        if self.tick_label_pad is not None:
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)

        # Tick rotation
        if self.x_tick_rotation is not None:
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
        if self.y_tick_rotation is not None:
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
        if self.z_tick_rotation is not None:
            self.ax.tick_params(axis='z', rotation=self.z_tick_rotation)

    def method_scale(self):
        # Scaling
        max_scale = max([self.x_scale, self.y_scale, self.z_scale])
        x_scale = self.x_scale / max_scale
        y_scale = self.y_scale / max_scale
        z_scale = self.z_scale / max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.ax.get_proj = lambda: np.dot(Axes3D.get_proj(self.ax), np.diag([x_scale, y_scale, z_scale, 1]))

    def method_resize_axes(self):
        if self.resize_axes is True:

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
                    v = [self.x_lower_bound, self.x_upper_bound]
                if isinstance(v[0], type(None)):
                    v[0] = l
                if isinstance(v[1], type(None)):
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
                pad_x = 0.05 * (abs(self.x.max()) + abs(self.x.min()))
                self.x_upper_resize_pad = pad_x
                self.x_lower_resize_pad = pad_x
                pad_y = 0.05 * (abs(self.y.max()) + abs(self.y.min()))
                self.y_upper_resize_pad = pad_y
                self.y_lower_resize_pad = pad_y
                pad_z = 0.05 * (abs(self.z.max()) + abs(self.z.min()))
                self.z_upper_resize_pad = pad_z
                self.z_lower_resize_pad = pad_z

            self.ax.set_xlim3d(self.x_bounds[0] - self.x_lower_resize_pad,
                               self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ylim3d(self.y_bounds[0] - self.y_lower_resize_pad,
                               self.y_bounds[1] + self.y_upper_resize_pad)
            self.ax.set_zlim3d(self.z_bounds[0] - self.y_lower_resize_pad,
                               self.z_bounds[1] + self.y_upper_resize_pad)


class plot(canvas, attributes):

    def init(self):
        if not isinstance(self.backend, type(None)):
            try:
                mpl.use(self.backend)
            except AttributeError:
                raise AttributeError(
                    '{} backend not supported with current Python configuration'.format(self.backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

        self.plt = import_module("matplotlib.pyplot")

        self.run()

    def main(self):
        # Canvas setup
        self.method_style()
        self.method_setup()

        # Scale axes
        self.method_scale()

        # Mock plot
        self.mock()

        # Plot
        self.plot()

    def finish(self):
        # Legend
        plot_label=None,
        self.method_legend()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_background_color()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()
        self.method_pane_fill()

        # Save
        self.method_save()

        self.method_show()

    def run(self):
        self.main()
        try:
            self.custom()
        except AttributeError:
            pass
        self.finish()

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
            if isinstance(self.norm, type(None)):
                return print_color("No norm selected for colorbar. Set norm=<parameter of choice>", "grey")

            # Obtain and apply limits
            if isinstance(self.cb_vmin, type(None)):
                self.cb_vmin = self.norm.min()
            if isinstance(self.cb_vmax, type(None)):
                self.cb_vmax = self.norm.max()
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
                                     format='%.' + str(self.tick_ndecimals) + 'f',
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
                if not isinstance(self.cb_title,
                                  type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                    print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
                if self.cb_y_title is True:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_ytitle_labelpad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                if self.cb_top_title is True:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_top_title_pad)
                    cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title_size)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size,
                                                       weight=self.cb_title_weight)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)


class surf(color):

    def custom(self):
        self.method_cb()
        self.method_edges_to_rgba()
        self.method_lighting()

    def method_lighting(self):
        ls = LightSource(270, 45)
        rgb = ls.shade(self.z, cmap=cm.get_cmap(self.cmap), vert_exag=0.1, blend_mode='soft')
        return rgb

    def method_edges_to_rgba(self):
        if self.edges_to_rgba is True:
            self.graph.set_edgecolors(self.graph.to_rgba(self.graph._A))


class line(plot):

    def __init__(self,
                 # Specifics
                 line_width=5,
                 # Input
                 x=None, x_scale=1,
                 y=None, y_scale=1,
                 z=None, z_scale=1,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black",
                 # Figure, axis
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111, azim=54, elev=25,
                 # Setup
                 prune=None, resize_axes=True, aspect=1, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None,
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
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=1,
                 # Title
                 title=None, title_weight=None, title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_bold=False, z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 z_tick_number=5, z_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None, tick_label_pad=4, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=8.5, tick_label_size_x=None, tick_label_size_y=None, tick_label_size_z=None,
                 # Color bar
                 color_bar=False, extend='neither', shrink=0.75,
                 cb_title=None, cb_axis_labelpad=10, cb_tick_number=5,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10,
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

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(line).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = self.x if isinstance(self.x, type(None)) or isinstance(self.x, np.ndarray) else np.array(self.x)
        self.y = self.y if isinstance(self.y, type(None)) or isinstance(self.y, np.ndarray) else np.array(self.y)
        self.z = self.z if isinstance(self.z, type(None)) or isinstance(self.z, np.ndarray) else np.array(self.z)

        self.init()

    def plot(self):

        self.graph = self.ax.plot3D(self.x, self.y, self.z, alpha=self.alpha, linewidth=self.line_width,
                                    color=self.color, label=self.plot_label)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)) and isinstance(self.z, type(None)):
            self.x = np.linspace(-2, 2, 1000)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)


class scatter(plot, color):

    def __init__(self,
                 # Specifics
                 point_size=5,
                 marker="o",
                 # Input
                 x=None, x_scale=1,
                 y=None, y_scale=1,
                 z=None, z_scale=1,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black",
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111, azim=54, elev=25,
                 # Setup
                 prune=None, resize_axes=True, aspect=1, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None,
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
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=1, norm=None,
                 # Title
                 title=None, title_weight=None, title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_bold=False, z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 z_tick_number=5, z_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None, tick_label_pad=4, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=8.5, tick_label_size_x=None, tick_label_size_y=None, tick_label_size_z=None,
                 # Color bar
                 color_bar=False, cb_pad=0.1, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
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

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(scatter).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = self.x if isinstance(self.x, type(None)) or isinstance(self.x, np.ndarray) else np.array(self.x)
        self.y = self.y if isinstance(self.y, type(None)) or isinstance(self.y, np.ndarray) else np.array(self.y)
        self.z = self.z if isinstance(self.z, type(None)) or isinstance(self.z, np.ndarray) else np.array(self.z)

        self.init()

    def plot(self):

        if not isinstance(self.norm, type(None)):
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.point_size, marker=self.marker,
                                         c=self.norm, cmap=self.cmap,
                                         alpha=self.alpha)
            self.method_cb()
        else:
            self.graph = self.ax.scatter(self.x, self.y, self.z, label=self.plot_label,
                                         s=self.point_size, marker=self.marker,
                                         color=self.color,
                                         alpha=self.alpha)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)) and isinstance(self.z, type(None)):
            self.x = np.linspace(-2, 2, 20)
            self.y = np.sin(self.x)
            self.z = np.cos(self.x)
            self.norm = self.z


class surface(plot, surf):

    def __init__(self,
                 # Specifics: surface
                 edge_color='b', edges_to_rgba=True, rstride=1, cstride=1, line_width=0,
                 # Specifics: lighting
                 lighting=False, antialiased=False, shade=False,
                 # Specifics: color
                 norm=None, c=None,
                 # Input
                 x=None, x_scale=1,
                 y=None, y_scale=1,
                 z=None, z_scale=1,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black",
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111, azim=54, elev=25,
                 # Setup
                 prune=None, resize_axes=True, aspect=1, box_to_plot_pad=10,
                 # Spines
                 spines_juggled=(1, 0, 2), spine_color=None,
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
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Color
                 color='darkred', cmap='RdBu_r', alpha=1,
                 # Title
                 title=None, title_weight=None, title_size=12, title_y=1.025, title_color=None, title_font=None,
                 # Labels
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=7, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=7, y_label_rotation=None,
                 z_label='z', z_label_bold=False, z_label_size=12, z_label_pad=7, z_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 z_tick_number=5, z_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None, tick_label_pad=4, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=8.5, tick_label_size_x=None, tick_label_size_y=None, tick_label_size_z=None,
                 # Color bar
                 color_bar=False, cb_pad=0.1, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
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

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(surface).parameters:
            setattr(self, item, eval(item))

        # Coordinates
        self.x = self.x if isinstance(self.x, type(None)) or isinstance(self.x, np.ndarray) else np.array(self.x)
        self.y = self.y if isinstance(self.y, type(None)) or isinstance(self.y, np.ndarray) else np.array(self.y)
        self.z = self.z if isinstance(self.z, type(None)) or isinstance(self.z, np.ndarray) else np.array(self.z)

        self.init()

    def plot(self):
        self.graph = self.ax.plot_surface(self.x, self.y, self.z, cmap=self.cmap,
                                          edgecolors=self.edge_color, alpha=self.alpha,
                                          rstride=self.rstride, cstride=self.cstride, linewidth=self.line_width,
                                          norm=self.norm, facecolors=self.method_lighting() if self.lighting is True else None,
                                          antialiased=self.antialiased, shade=self.shade,
                                          )
        self.ax.view_init(azim=self.azim, elev=self.elev)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)) and isinstance(self.z, type(None)):
            self.x, self.y, self.z = MockData().hill()


def floating_text(ax, text, font, x, y, z, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, z, text, size=size, weight=weight, fontdict=font)
