import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import colors
from matplotlib import cm

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib.ticker import FormatStrFormatter
import matplotlib.dates as mdates

from numpy import sin, cos
from skimage import measure

import matplotlib.font_manager as font_manager

from pylab import floor

from mpl_plotter.resources.functions import print_color
from mpl_plotter.resources.colormaps import ColorMaps
from mpl_plotter.resources.mock_data import MockData


class line:

    """
    :param x:
    :param x_scale:
    :param x_pad:
    :param x_bounds:
    :param y:
    :param y_scale:
    :param y_pad:
    :param y_bounds:
    :param z:
    :param z_scale:
    :param z_pad:
    :param z_bounds:
    :param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                    Backend error:
                        pip install pyqt5
                        pip install tkinter
                        pip install tk
                        ... stackoverflow
                    Plotting window freezes even if trying different backends with no backend error: python configuration problem
                        backend=None
    :param fig:
    :param ax:
    :param figsize:
    :param shape_and_position:
    :param font:
    :param light:
    :param dark:
    :param pane_fill:
    :param box_to_plot_pad:
    :param color:
    :param workspace_color:
    :param workspace_color2:
    :param line_width:
    :param label:
    :param legend:
    :param legend_loc:
    :param legend_size:
    :param legend_weight:
    :param legend_style:
    :param grid:
    :param grid_color:
    :param grid_lines:
    :param spines_removed:
    :param cmap:
    :param alpha:
    :param color_bar:
    :param extend:
    :param cb_title:
    :param cb_axis_labelpad:
    :param cb_nticks:
    :param shrink:
    :param cb_outline_width:
    :param cb_title_rotation:
    :param cb_title_style:
    :param cb_title_size:
    :param cb_top_title_y:
    :param cb_ytitle_labelpad:
    :param cb_title_weight:
    :param cb_top_title:
    :param cb_y_title:
    :param cb_top_title_pad:
    :param cb_top_title_x:
    :param cb_vmin:
    :param cb_vmax:
    :param cb_ticklabelsize:
    :param prune:
    :param resize_axes:
    :param aspect:
    :param title:
    :param title_bold:
    :param title_size:
    :param title_y:
    :param x_label:
    :param x_label_bold:
    :param x_label_size:
    :param x_label_pad:
    :param x_label_rotation:
    :param y_label:
    :param y_label_bold:
    :param y_label_size:
    :param y_label_pad:
    :param y_label_rotation:
    :param z_label:
    :param z_label_bold:
    :param z_label_size:
    :param z_label_pad:
    :param z_label_rotation:
    :param x_tick_number:
    :param x_tick_labels:
    :param y_tick_number:
    :param y_tick_labels:
    :param z_tick_number:
    :param z_tick_labels:
    :param x_tick_rotation:
    :param y_tick_rotation:
    :param z_tick_rotation:
    :param tick_color:
    :param tick_label_pad:
    :param tick_ndecimals:
    :param tick_label_size:
    :param tick_label_size_x:
    :param tick_label_size_y:
    :param tick_label_size_z:
    :param more_subplots_left:
    :param filename:
    :param dpi:
    """

    def __init__(self,
                 x=None, x_scale=1, x_pad=0, x_bounds=None,
                 y=None, y_scale=1, y_pad=0, y_bounds=None,
                 z=None, z_scale=1, z_pad=0, z_bounds=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, pane_fill=None,
                 box_to_plot_pad=10,
                 color='darkred', workspace_color=None, workspace_color2=None,
                 line_width=5,
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', alpha=None, color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10,
                 shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=1,
                 title='Line', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 z_label='z', z_label_bold=False, z_label_size=12, z_label_pad=5, z_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=None, y_tick_labels=None,
                 z_tick_number=None, z_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, z_tick_rotation=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None, tick_label_size_z=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 ):

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.line_width = line_width

        # Coordinates
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.x_scale = x_scale
        self.x_bounds = x_bounds
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.y_scale = y_scale
        self.y_bounds = y_bounds
        self.z = z if isinstance(z, type(None)) or isinstance(z, np.ndarray) else np.array(z)
        self.z_scale = z_scale
        self.z_bounds = z_bounds
        # Base
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        # Legend
        self.label = label
        self.legend = legend
        self.legend_loc = legend_loc
        self.legend_size = legend_size
        self.legend_weight = legend_weight
        self.legend_style = legend_style
        self.legend_handleheight = legend_handleheight
        self.legend_ncol = legend_ncol
        # Grid
        self.grid = grid
        self.grid_color = grid_color
        self.grid_lines = grid_lines
        # Workspace color
        self.workspace_color = workspace_color
        self.workspace_color2 = workspace_color2
        self.pane_fill = pane_fill
        # Plot color
        self.color = color
        self.cmap = cmap
        self.alpha = alpha
        # Color bar
        self.color_bar = color_bar
        self.extend = extend
        self.cb_title = cb_title
        self.cb_axis_labelpad = cb_axis_labelpad
        self.cb_nticks = cb_nticks
        self.shrink = shrink
        self.cb_outline_width = cb_outline_width
        self.cb_title_rotation = cb_title_rotation
        self.cb_title_style = cb_title_style
        self.cb_title_size = cb_title_size
        self.cb_top_title_y = cb_top_title_y
        self.cb_ytitle_labelpad = cb_ytitle_labelpad
        self.cb_title_weight = cb_title_weight
        self.cb_top_title = cb_top_title
        self.cb_y_title = cb_y_title
        self.cb_top_title_pad = cb_top_title_pad
        self.cb_top_title_x = cb_top_title_x
        self.cb_vmin = cb_vmin
        self.cb_vmax = cb_vmax
        self.cb_ticklabelsize = cb_ticklabelsize
        # Axes
        self.resize_axes = resize_axes
        self.aspect = aspect
        self.prune = prune
        self.x_pad = x_pad
        self.y_pad = y_pad
        self.z_pad = z_pad
        self.box_to_plot_pad = box_to_plot_pad
        # Spines
        self.spines_removed = spines_removed
        # Title
        self.title = title
        self.title_bold = title_bold
        self.title_size = title_size
        self.title_y = title_y
        # Axis labels
        self.x_label = x_label
        self.x_label_bold = x_label_bold
        self.x_label_size = x_label_size
        self.x_label_pad = x_label_pad
        self.x_label_rotation = x_label_rotation
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        self.z_label = z_label
        self.z_label_bold = z_label_bold
        self.z_label_size = z_label_size
        self.z_label_pad = z_label_pad
        self.z_label_rotation = z_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.y_tick_rotation = y_tick_rotation
        self.z_tick_number = z_tick_number
        self.z_tick_labels = z_tick_labels
        self.z_tick_rotation = z_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.tick_label_size_z = tick_label_size_z
        # Display and save
        self.more_subplots_left = more_subplots_left
        self.newplot = newplot
        self.filename = filename
        self.dpi = dpi

        self.main()

    def main(self):

        self.method_style()

        self.method_setup()

        # Mock plot
        self.method_mock()

        # Plot
        self.graph = self.ax.plot3D(self.x, self.y, self.z, alpha=self.alpha, linewidth=self.line_width,
                                    color=self.color, label=self.label)

        # Legend
        self.method_legend()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_background_alpha()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()
        self.method_pane_fill()

        # Save
        self.method_save()

        self.method_show()

        return self.ax

    def method_figure(self):
        if not isinstance(self.style, type(None)):
            plt.style.use(self.style)
        self.fig = plt.figure(figsize=self.figsize)

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
        if not isinstance(plt.gcf(), type(None)):
            if self.newplot is True:
                self.method_figure()
            else:
                self.fig = plt.gcf()
        else:
            self.method_figure()

        if plt.gca().name == '3d':
            if isinstance(self.ax, type(None)):
               self.ax = plt.gca()
        else:
            plt.gca().remove()
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box', projection='3d')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)) and isinstance(self.z, type(None)):
            self.x, self.y = MockData().sinewave()
            self.z = np.array([5])

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            self.ax.legend(loc=self.legend_loc, prop=legend_font,
                           handleheight=self.legend_handleheight, ncol=self.legend_ncol)

    def method_resize_axes(self):
        if self.resize_axes is True:
            self.z_pad = self.z_pad if self.z_pad > (abs(self.z.max()) + abs(self.z.min())) / 16 else (abs(self.z.max()) + abs(self.z.min())) / 16
            if isinstance(self.x_bounds, type(None)):
                self.x_bounds = (self.x.min(), self.x.max())
            if isinstance(self.y_bounds, type(None)):
                self.y_bounds = (self.y.min(), self.y.max())
            if isinstance(self.z_bounds, type(None)):
                self.z_bounds = (self.z.min(), self.z.max())
            self.ax.set_xlim3d(self.x_bounds[0] - self.x_pad, self.x_bounds[1] + self.x_pad)
            self.ax.set_ylim3d(self.y_bounds[0] - self.y_pad, self.y_bounds[1] + self.y_pad)
            self.ax.set_zlim3d(self.z_bounds[0] - self.z_pad, self.z_bounds[1] + self.z_pad)

    def method_save(self):
        if self.filename:
            plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.more_subplots_left is not True:
            self.fig.tight_layout()
            plt.show()
        else:
            print('Ready for next subplot')

    def method_background_alpha(self):
        self.ax.patch.set_alpha(1)

    def method_title(self):
        if not isinstance(self.title, type(None)):
            if self.title_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_title(self.title, y=self.title_y, fontname=self.font, weight=weight,
                              color=self.workspace_color, size=self.title_size)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if not isinstance(self.x_label, type(None)):
            if self.x_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.x_label_size, labelpad=self.x_label_pad,
                               rotation=self.x_label_rotation)
        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
        if not isinstance(self.z_label, type(None)):
            if self.z_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_zlabel(self.z_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.z_label_size, labelpad=self.z_label_pad,
                               rotation=self.z_label_rotation)

    def method_spines(self):
        spine_color = self.workspace_color
        for spine in self.ax.spines.values():
            spine.set_color(spine_color)

        top = True
        right = True
        left = True
        bottom = True

        for spine in self.spines_removed:
            self.ax.spines[spine].set_visible(False)
            if spine == 'top':
                top = False
            if spine == 'bottom':
                bottom=False
            if spine == 'left':
                left = False
            if spine == 'right':
                right = False

        self.ax.tick_params(axis='both', which='both', top=top, right=right, left=left, bottom=bottom)

    def method_ticks(self):
        #   Color
        if self.tick_color is not None:
            self.ax.tick_params(axis='both', color=self.tick_color)

            self.ax.w_xaxis.line.set_color(self.tick_color)
            self.ax.w_yaxis.line.set_color(self.tick_color)
            self.ax.w_zaxis.line.set_color(self.tick_color)
        #   Label size
        if self.tick_label_size is not None:
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Numeral size
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
        for tick in self.ax.get_zticklabels():
            tick.set_fontname(self.font)
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.zaxis.set_major_formatter(FormatStrFormatter(float_format))

        # Tick number
        if self.x_tick_number is not None:
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(self.x_tick_number, prune=self.prune))
        if self.y_tick_number is not None:
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(self.y_tick_number, prune=self.prune))
        if self.z_tick_number is not None:
            self.ax.zaxis.set_major_locator(plt.MaxNLocator(self.z_tick_number, prune=self.prune))

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

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)

    def method_pane_fill(self):
        # Pane fill and pane edge color
        self.ax.xaxis.pane.fill = self.pane_fill
        self.ax.yaxis.pane.fill = self.pane_fill
        self.ax.zaxis.pane.fill = self.pane_fill
        self.ax.xaxis.pane.set_edgecolor(self.tick_color)
        self.ax.yaxis.pane.set_edgecolor(self.tick_color)


def floating_text(ax, text, font, x, y, z, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, z, text, size=size, weight=weight, fontdict=font)
