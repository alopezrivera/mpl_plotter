import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import colors
from matplotlib.ticker import FormatStrFormatter
from matplotlib import dates as mdates

from numpy import sin, cos
from skimage import measure

from matplotlib import cm
from matplotlib import ticker
from matplotlib import font_manager as font_manager

from pylab import floor

from mpl_plotter.resources.mock_data import MockData
from mpl_plotter.resources.functions import normalize
from mpl_plotter.resources.functions import print_color


class line:

    def __init__(self,
                 x=None, y=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, zorder=None,
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 color=None, workspace_color=None, workspace_color2=None, alpha=None, norm=None,
                 line_width=3,
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10,
                 shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=None,
                 title='Spirograph', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=10, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,

                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d'
                 ):

        """
        :param x:
        :param y:
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
        :param x_upper_bound:
        :param x_lower_bound:
        :param y_upper_bound:
        :param y_lower_bound:
        :param x_upper_resize_pad:
        :param x_lower_resize_pad:
        :param y_upper_resize_pad:
        :param y_lower_resize_pad:
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
        :param x_tick_number:
        :param x_tick_labels:
        :param y_tick_number:
        :param y_tick_labels:
        :param x_tick_rotation:
        :param y_tick_rotation:
        :param x_label_coords:
        :param y_label_coords:
        :param tick_color:
        :param tick_label_pad:
        :param tick_ndecimals:
        :param tick_label_size:
        :param tick_label_size_x:
        :param tick_label_size_y:
        :param more_subplots_left:
        :param filename:
        :param dpi:
        :param custom_x_tick_labels:
        :param custom_y_tick_labels:
        :param date_tick_labels_x:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.line_width = line_width

        # Base
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.zorder = zorder
        self.x_upper_bound = y_bounds[1] if not isinstance(x_bounds, type(None)) else x_upper_bound
        self.x_lower_bound = y_bounds[0] if not isinstance(x_bounds, type(None)) else x_lower_bound
        self.y_upper_bound = y_bounds[1] if not isinstance(y_bounds, type(None)) else y_upper_bound
        self.y_lower_bound = y_bounds[0] if not isinstance(y_bounds, type(None)) else y_lower_bound
        self.x_upper_resize_pad = x_upper_resize_pad
        self.x_lower_resize_pad = x_lower_resize_pad
        self.y_upper_resize_pad = y_upper_resize_pad
        self.y_lower_resize_pad = y_lower_resize_pad
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
        # Plot color
        self.color = color
        self.cmap = cmap
        self.alpha = alpha
        self.norm = norm
        # Color bar
        self.color_bar = color_bar
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
        self.x_label_coords = x_label_coords
        self.y_label_coords = y_label_coords
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_rotation = y_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.custom_x_tick_labels = custom_x_tick_labels
        self.custom_y_tick_labels = custom_y_tick_labels
        self.date_tick_labels_x = date_tick_labels_x
        self.date_format = date_format
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
        self.graph = self.ax.plot(self.x, self.y, label=self.label, linewidth=self.line_width, color=self.color,
                                  zorder=self.zorder,
                                  alpha=self.alpha,
                                  )

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

        if not isinstance(plt.gca(), type(None)):
            if isinstance(self.ax, type(None)):
               self.ax = plt.gca()
        else:
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()

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
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad, upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad, upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

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
            self.ax.set_title(self.title, fontname=self.font, weight=weight,
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
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

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
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(
                self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(
                self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        #       Date tick labels
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


class scatter:

    def __init__(self,
                 x=None, y=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, zorder=None,
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 color=None, workspace_color=None, workspace_color2=None, alpha=None, norm=None, c=None,
                 point_size=5, marker='o',
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None, cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=None,
                 title='Spirograph', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=10, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d'
                 ):

        """
        :param x:
        :param y:
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
        :param x_upper_bound:
        :param x_lower_bound:
        :param y_upper_bound:
        :param y_lower_bound:
        :param x_upper_resize_pad:
        :param x_lower_resize_pad:
        :param y_upper_resize_pad:
        :param y_lower_resize_pad:
        :param color:
        :param workspace_color:
        :param workspace_color2:
        :param c:
        :param point_size:
        :param marker:
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
        :param x_tick_number:
        :param x_tick_labels:
        :param y_tick_number:
        :param y_tick_labels:
        :param x_tick_rotation:
        :param y_tick_rotation:
        :param x_label_coords:
        :param y_label_coords:
        :param tick_color:
        :param tick_label_pad:
        :param tick_ndecimals:
        :param tick_label_size:
        :param tick_label_size_x:
        :param tick_label_size_y:
        :param more_subplots_left:
        :param filename:
        :param dpi:
        :param custom_x_tick_labels:
        :param custom_y_tick_labels:
        :param date_tick_labels_x:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.point_size = point_size
        self.marker = marker

        # Base
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.zorder = zorder
        self.x_upper_bound = y_bounds[1] if not isinstance(x_bounds, type(None)) else x_upper_bound
        self.x_lower_bound = y_bounds[0] if not isinstance(x_bounds, type(None)) else x_lower_bound
        self.y_upper_bound = y_bounds[1] if not isinstance(y_bounds, type(None)) else y_upper_bound
        self.y_lower_bound = y_bounds[0] if not isinstance(y_bounds, type(None)) else y_lower_bound
        self.x_upper_resize_pad = x_upper_resize_pad
        self.x_lower_resize_pad = x_lower_resize_pad
        self.y_upper_resize_pad = y_upper_resize_pad
        self.y_lower_resize_pad = y_lower_resize_pad
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
        # Plot color
        self.color = color
        self.c = c
        self.cmap = cmap
        self.alpha = alpha
        self.norm = norm
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
        self.x_label_coords = x_label_coords
        self.y_label_coords = y_label_coords
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_rotation = y_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.custom_x_tick_labels = custom_x_tick_labels
        self.custom_y_tick_labels = custom_y_tick_labels
        self.date_tick_labels_x = date_tick_labels_x
        self.date_format = date_format
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

        # Color
        if isinstance(self.color, type(None)) and isinstance(self.c, type(None)):
            print_color(f'No color or color key provided. Reverting to grey', 'grey')
            self.color = self.workspace_color2

        # Plot
        if not isinstance(self.color, type(None)):
            self.graph = self.ax.scatter(self.x, self.y, label=self.label, s=self.point_size, marker=self.marker,
                                         color=self.color,
                                         zorder=self.zorder,
                                         alpha=self.alpha)
        if not isinstance(self.c, type(None)):
            self.graph = self.ax.scatter(self.x, self.y, label=self.label, s=self.point_size, marker=self.marker,
                                         c=self.c, cmap=self.cmap,
                                         zorder=self.zorder,
                                         alpha=self.alpha)

        # Colorbar
        self.method_cb()

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
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = None

    def method_setup(self):
        if not isinstance(plt.gcf(), type(None)):
            if self.newplot is True:
                self.method_figure()
            else:
                self.fig = plt.gcf()
        else:
            self.method_figure()

        if not isinstance(plt.gca(), type(None)):
            if isinstance(self.ax, type(None)):
                self.ax = plt.gca()
        else:
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()

    def method_cb(self):
        if self.color_bar is True:
            # Apply limits if any
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            if not isinstance(self.cb_vmin, type(None)) and isinstance(self.cb_vmax, type(None)):
                locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_nticks, endpoint=True)
            else:
                locator = ticker.MaxNLocator(nbins=self.cb_nticks)

            # Colorbar
            cbar = self.fig.colorbar(self.graph, spacing='proportional', ticks=locator, shrink=self.shrink,
                                     extend=self.extend, norm=None, orientation='vertical',
                                     ax=self.ax,
                                     format='%.' + str(self.tick_ndecimals) + 'f')

            # Ticks
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Title
            if not isinstance(self.cb_title, type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
            if self.cb_y_title is True:
                cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.yaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, size=self.cb_title_size,
                                                              weight=self.cb_title_weight)
                text.set_font_properties(font)
            if self.cb_top_title is True:
                cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                                  'horizontalalignment': 'left'},
                                  pad=self.cb_top_title_pad)
                cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                text = cbar.ax.title
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, weight=self.cb_title_weight,
                                                              size=self.cb_title_size)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            leg = self.ax.legend(loc=self.legend_loc, prop=legend_font,
                                 handleheight=self.legend_handleheight, ncol=self.legend_ncol)
            if not isinstance(self.c, type(None)):
                leg.legendHandles[0].set_color(cm.get_cmap(self.cmap)((np.clip(self.c.mean(), self.c.min(), self.c.max()) - self.c.min())/(self.c.max()-self.c.min())))

    def method_resize_axes(self):
        if self.resize_axes is True:
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05 * (self.x_upper_bound - self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05 * (self.x_upper_bound - self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05 * (self.y_upper_bound - self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05 * (self.y_upper_bound - self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad,
                               upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad,
                               upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

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
            self.ax.set_title(self.title, fontname=self.font, weight=weight,
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
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

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
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                                           self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                                           self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                                           self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                                           self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


class heatmap:

    def __init__(self,
                 x=None, y=None, z=None, array=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, zorder=None,
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 color=None, workspace_color=None, workspace_color2=None, alpha=None,
                 norm=None, normvariant='SymLog',
                 cmap='RdBu_r', color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None, cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=None,
                 title='Water drop function', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=10, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d'
                 ):

        """
        :param x:
        :param y:
        :param z:
        :param array:
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
        :param x_upper_bound:
        :param x_lower_bound:
        :param y_upper_bound:
        :param y_lower_bound:
        :param x_upper_resize_pad:
        :param x_lower_resize_pad:
        :param y_upper_resize_pad:
        :param y_lower_resize_pad:
        :param grid:
        :param grid_color:
        :param grid_lines:
        :param spines_removed:
        :param color:
        :param workspace_color:
        :param workspace_color2:
        :param norm:
        :param normvariant:
        :param cmap:
        :param color_bar:
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
        :param x_tick_number:
        :param x_tick_labels:
        :param y_tick_number:
        :param y_tick_labels:
        :param x_tick_rotation:
        :param y_tick_rotation:
        :param x_label_coords:
        :param y_label_coords:
        :param tick_color:
        :param tick_label_pad:
        :param tick_ndecimals:
        :param tick_label_size:
        :param tick_label_size_x:
        :param tick_label_size_y:
        :param more_subplots_left:
        :param filename:
        :param dpi:
        :param custom_x_tick_labels:
        :param custom_y_tick_labels:
        :param date_tick_labels_x:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics

        # Base
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.z = z if not isinstance(z, type(None)) else array
        self.array = array
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.zorder = zorder
        self.x_upper_bound = y_bounds[1] if not isinstance(x_bounds, type(None)) else x_upper_bound
        self.x_lower_bound = y_bounds[0] if not isinstance(x_bounds, type(None)) else x_lower_bound
        self.y_upper_bound = y_bounds[1] if not isinstance(y_bounds, type(None)) else y_upper_bound
        self.y_lower_bound = y_bounds[0] if not isinstance(y_bounds, type(None)) else y_lower_bound
        self.x_upper_resize_pad = x_upper_resize_pad
        self.x_lower_resize_pad = x_lower_resize_pad
        self.y_upper_resize_pad = y_upper_resize_pad
        self.y_lower_resize_pad = y_lower_resize_pad
        # Grid
        self.grid = grid
        self.grid_color = grid_color
        self.grid_lines = grid_lines
        # Normalization
        self.norm = norm
        self.normvariant = normvariant
        # Workspace color
        self.workspace_color = workspace_color
        self.workspace_color2 = workspace_color2
        # Plot color
        self.color = color
        self.cmap = cmap
        self.alpha = alpha
        self.norm = norm
        # Color bar
        self.color_bar = color_bar
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
        self.x_label_coords = x_label_coords
        self.y_label_coords = y_label_coords
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_rotation = y_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.custom_x_tick_labels = custom_x_tick_labels
        self.custom_y_tick_labels = custom_y_tick_labels
        self.date_tick_labels_x = date_tick_labels_x
        self.date_format = date_format
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

        # Normalize
        self.method_normalize()

        # Plot
        try:
            self.graph = self.ax.pcolormesh(self.x, self.y, self.z, cmap=self.cmap,
                                            zorder=self.zorder,
                                            alpha=self.alpha,
                                            )
        except:
            try:
                self.graph = self.ax.pcolormesh(self.z, cmap=self.cmap, norm=self.norm,
                                                zorder=self.zorder,
                                                alpha=self.alpha)
            except:
                # Mock plot
                self.z = MockData().waterdropdf()
                self.graph = self.ax.pcolormesh(self.z, cmap=self.cmap, norm=self.norm,
                                                zorder=self.zorder,
                                                alpha=self.alpha)

        # Maximum and minimum
        self.method_max_min()

        # Colorbar
        self.method_cb()

        # Resize axes
        self.method_resize_axes()

        # Makeup
        self.method_background_alpha()
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()
        self.method_grid()

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
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = None

    def method_setup(self):
        if not isinstance(plt.gcf(), type(None)):
            if self.newplot is True:
                self.method_figure()
            else:
                self.fig = plt.gcf()
        else:
            self.method_figure()

        if not isinstance(plt.gca(), type(None)):
            if isinstance(self.ax, type(None)):
                self.ax = plt.gca()
        else:
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.array = MockData().waterdropdf()

    def method_normalize(self):
        if self.norm is not None:
            self.norm = normalize(array=self.array, norm=self.norm, variant=self.normvariant)

    def method_max_min(self):
        if not isinstance(self.array, type(None)):
            xmin = 0
            ymin = 0
            xmax = self.array.shape[0]
            ymax = self.array.shape[1]
            if self.resize_axes is True and isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = xmax
            if self.resize_axes is True and isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = xmin
            if self.resize_axes is True and isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = ymax
            if self.resize_axes is True and isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = ymin

    def method_cb(self):
        if self.color_bar is True:
            # Apply limits if any
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            if not isinstance(self.cb_vmin, type(None)) and isinstance(self.cb_vmax, type(None)):
                locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_nticks, endpoint=True)
            else:
                locator = ticker.MaxNLocator(nbins=self.cb_nticks)

            # Colorbar
            cbar = self.fig.colorbar(self.graph, spacing='proportional', ticks=locator, shrink=self.shrink,
                                     extend=self.extend, norm=None, orientation='vertical',
                                     ax=self.ax,
                                     format='%.' + str(self.tick_ndecimals) + 'f')

            # Ticks
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Title
            if not isinstance(self.cb_title, type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
            if self.cb_y_title is True:
                cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.yaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, size=self.cb_title_size,
                                                              weight=self.cb_title_weight)
                text.set_font_properties(font)
            if self.cb_top_title is True:
                cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                                  'horizontalalignment': 'left'},
                                  pad=self.cb_top_title_pad)
                cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                text = cbar.ax.title
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, weight=self.cb_title_weight,
                                                              size=self.cb_title_size)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_resize_axes(self):
        if self.resize_axes is True:
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad,
                               upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad,
                               upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

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
            self.ax.set_title(self.title, fontname=self.font, weight=weight,
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
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

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
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                                           self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                                           self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                                           self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                                           self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


class quiver:

    def __init__(self,
                 x=None, y=None, u=None, v=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, zorder=None,
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 color=None, workspace_color=None, workspace_color2=None, alpha=None, norm=None,
                 rule=None, custom_rule=None, vector_width=0.01, vector_min_shaft=2, vector_length_threshold=0.1,
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None, cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=None,
                 title='Quiver', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=10, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,

                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d'
                 ):

        """
        :param x:
        :param y:
        :param u:
        :param v:
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
        :param x_upper_bound:
        :param x_lower_bound:
        :param y_upper_bound:
        :param y_lower_bound:
        :param x_upper_resize_pad:
        :param x_lower_resize_pad:
        :param y_upper_resize_pad:
        :param y_lower_resize_pad:
        :param color:
        :param workspace_color:
        :param workspace_color2:
        :param rule:
        :param custom_rule:
        :param vector_width:
        :param vector_min_shaft:
        :param vector_length_threshold:
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
        :param x_tick_number:
        :param x_tick_labels:
        :param y_tick_number:
        :param y_tick_labels:
        :param x_tick_rotation:
        :param y_tick_rotation:
        :param x_label_coords:
        :param y_label_coords:
        :param tick_color:
        :param tick_label_pad:
        :param tick_ndecimals:
        :param tick_label_size:
        :param tick_label_size_x:
        :param tick_label_size_y:
        :param more_subplots_left:
        :param filename:
        :param dpi:
        :param custom_x_tick_labels:
        :param custom_y_tick_labels:
        :param date_tick_labels_x:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.u = u
        self.v = v
        self.rule = rule
        self.custom_rule = custom_rule
        self.vector_width = vector_width
        self.vector_min_shaft = vector_min_shaft
        self.vector_length_threshold = vector_length_threshold

        # Base
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.zorder = zorder
        self.x_upper_bound = y_bounds[1] if not isinstance(x_bounds, type(None)) else x_upper_bound
        self.x_lower_bound = y_bounds[0] if not isinstance(x_bounds, type(None)) else x_lower_bound
        self.y_upper_bound = y_bounds[1] if not isinstance(y_bounds, type(None)) else y_upper_bound
        self.y_lower_bound = y_bounds[0] if not isinstance(y_bounds, type(None)) else y_lower_bound
        self.x_upper_resize_pad = x_upper_resize_pad
        self.x_lower_resize_pad = x_lower_resize_pad
        self.y_upper_resize_pad = y_upper_resize_pad
        self.y_lower_resize_pad = y_lower_resize_pad
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
        # Plot color
        self.color = color
        self.cmap = cmap
        self.alpha = alpha
        self.norm = norm
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
        self.x_label_coords = x_label_coords
        self.y_label_coords = y_label_coords
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_rotation = y_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.custom_x_tick_labels = custom_x_tick_labels
        self.custom_y_tick_labels = custom_y_tick_labels
        self.date_tick_labels_x = date_tick_labels_x
        self.date_format = date_format
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

        # Color rule
        self.method_rule()

        # Plot
        self.graph = self.ax.quiver(self.x, self.y, self.u, self.v,
                                    color=self.c, cmap=self.cmap,
                                    width=self.vector_width,
                                    minshaft=self.vector_min_shaft,
                                    minlength=self.vector_length_threshold,
                                    label=self.label,
                                    zorder=self.zorder,
                                    alpha=self.alpha
                                    )

        # Colorbar
        self.method_cb()

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
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = None

    def method_setup(self):
        if not isinstance(plt.gcf(), type(None)):
            if self.newplot is True:
                self.method_figure()
            else:
                self.fig = plt.gcf()
        else:
            self.method_figure()

        if not isinstance(plt.gca(), type(None)):
            if isinstance(self.ax, type(None)):
                self.ax = plt.gca()
        else:
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.random.random(100)
            self.y = np.random.random(100)
            self.u = np.random.random(100)
            self.v = np.random.random(100)

    def method_rule(self):
        # Rule
        if isinstance(self.custom_rule, type(None)):
            if isinstance(self.rule, type(None)):
                self.rule = lambda u, v: (u ** 2 + v ** 2)
            self.rule = self.rule(u=self.u, v=self.v)
        else:
            self.rule = self.custom_rule

        # Color determined by rule function
        c = self.rule
        # Flatten and normalize
        c = (c.ravel() - c.min()) / c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(self.cmap)
        self.c = cmap(c)

    def method_cb(self):
        if self.color_bar is True:
            # Apply limits if any
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            if not isinstance(self.cb_vmin, type(None)) and isinstance(self.cb_vmax, type(None)):
                locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_nticks, endpoint=True)
            else:
                locator = ticker.MaxNLocator(nbins=self.cb_nticks)

            # Colorbar
            cbar = self.fig.colorbar(self.graph, spacing='proportional', ticks=locator, shrink=self.shrink,
                                     extend=self.extend, norm=None, orientation='vertical',
                                     ax=self.ax,
                                     format='%.' + str(self.tick_ndecimals) + 'f')

            # Ticks
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Title
            if not isinstance(self.cb_title, type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
            if self.cb_y_title is True:
                cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.yaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, size=self.cb_title_size,
                                                              weight=self.cb_title_weight)
                text.set_font_properties(font)
            if self.cb_top_title is True:
                cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                                  'horizontalalignment': 'left'},
                                  pad=self.cb_top_title_pad)
                cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                text = cbar.ax.title
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, weight=self.cb_title_weight,
                                                              size=self.cb_title_size)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            leg = self.ax.legend(loc=self.legend_loc, prop=legend_font,
                                 handleheight=self.legend_handleheight, ncol=self.legend_ncol)
            leg.legendHandles[0].set_color(cm.get_cmap(self.cmap)((np.clip(self.c.mean(), self.c.min(), self.c.max()) - self.c.min())/(self.c.max()-self.c.min())))

    def method_resize_axes(self):
        if self.resize_axes is True:
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad, upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad, upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

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
            self.ax.set_title(self.title, fontname=self.font, weight=weight,
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
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

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
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                                           self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                                           self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                                           self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                                           self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


class streamline:

    def __init__(self,
                 x=None, y=None, u=None, v=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None, zorder=None,
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 color=None, workspace_color=None, workspace_color2=None, alpha=None, norm=None,
                 line_width=1, line_density=1,
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None, cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=None,
                 title='Streamlines', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=10, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False, newplot=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d'
                 ):

        """
        :param x:
        :param y:
        :param u:
        :param v:
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
        :param x_upper_bound:
        :param x_lower_bound:
        :param y_upper_bound:
        :param y_lower_bound:
        :param x_upper_resize_pad:
        :param x_lower_resize_pad:
        :param y_upper_resize_pad:
        :param y_lower_resize_pad:
        :param color:
        :param workspace_color:
        :param workspace_color2:
        :param line_width:
        :param line_density:
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
        :param x_tick_number:
        :param x_tick_labels:
        :param y_tick_number:
        :param y_tick_labels:
        :param x_tick_rotation:
        :param y_tick_rotation:
        :param x_label_coords:
        :param y_label_coords:
        :param tick_color:
        :param tick_label_pad:
        :param tick_ndecimals:
        :param tick_label_size:
        :param tick_label_size_x:
        :param tick_label_size_y:
        :param more_subplots_left:
        :param newplot:
        :param filename:
        :param dpi:
        :param custom_x_tick_labels:
        :param custom_y_tick_labels:
        :param date_tick_labels_x:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.u = u
        self.v = v
        self.line_width = line_width
        self.line_density = line_density

        # Base
        self.x = x if isinstance(x, type(None)) or isinstance(x, np.ndarray) else np.array(x)
        self.y = y if isinstance(y, type(None)) or isinstance(y, np.ndarray) else np.array(y)
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.zorder = zorder
        self.x_upper_bound = y_bounds[1] if not isinstance(x_bounds, type(None)) else x_upper_bound
        self.x_lower_bound = y_bounds[0] if not isinstance(x_bounds, type(None)) else x_lower_bound
        self.y_upper_bound = y_bounds[1] if not isinstance(y_bounds, type(None)) else y_upper_bound
        self.y_lower_bound = y_bounds[0] if not isinstance(y_bounds, type(None)) else y_lower_bound
        self.x_upper_resize_pad = x_upper_resize_pad
        self.x_lower_resize_pad = x_lower_resize_pad
        self.y_upper_resize_pad = y_upper_resize_pad
        self.y_lower_resize_pad = y_lower_resize_pad
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
        # Plot color
        self.color = color
        self.cmap = cmap
        self.alpha = alpha
        self.norm = norm
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
        self.x_label_coords = x_label_coords
        self.y_label_coords = y_label_coords
        self.y_label = y_label
        self.y_label_bold = y_label_bold
        self.y_label_size = y_label_size
        self.y_label_pad = y_label_pad
        self.y_label_rotation = y_label_rotation
        # Axis ticks
        self.x_tick_number = x_tick_number
        self.x_tick_labels = x_tick_labels
        self.y_tick_number = y_tick_number
        self.y_tick_labels = y_tick_labels
        self.x_tick_rotation = x_tick_rotation
        self.y_tick_rotation = y_tick_rotation
        self.tick_color = tick_color
        # Axis tick labels
        self.tick_label_pad = tick_label_pad
        self.tick_ndecimals = tick_ndecimals
        self.tick_label_size = tick_label_size
        self.tick_label_size_x = tick_label_size_x
        self.tick_label_size_y = tick_label_size_y
        self.custom_x_tick_labels = custom_x_tick_labels
        self.custom_y_tick_labels = custom_y_tick_labels
        self.date_tick_labels_x = date_tick_labels_x
        self.date_format = date_format
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

        # Color rule
        self.method_rule()

        # Plot
        self.graph = self.ax.streamplot(self.x, self.y, self.u, self.v,
                                        color=self.color,
                                        cmap=self.cmap,
                                        linewidth=self.line_width,
                                        density=self.line_density,
                                        zorder=self.zorder,
                                        alpha=self.alpha).lines

        # Colorbar
        self.method_cb()

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
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(None)) else self.workspace_color2
            self.style = None

    def method_setup(self):
        if not isinstance(plt.gcf(), type(None)):
            if self.newplot is True:
                self.method_figure()
            else:
                self.fig = plt.gcf()
        else:
            self.method_figure()

        if not isinstance(plt.gca(), type(None)):
            if isinstance(self.ax, type(None)):
                self.ax = plt.gca()
        else:
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.linspace(0, 10, 100)
            self.y = np.linspace(0, 10, 100)
            self.x, self.y = np.meshgrid(self.x, self.y)
            self.u = np.random.random(100)
            self.v = np.random.random(100)
            self.u, self.v = np.meshgrid(self.u, self.v)

    def method_rule(self):
        if isinstance(self.line_width, type(None)):
            rule_width = lambda u: 5*(u/u.max())**2
            self.line_width = rule_width(self.u)

    def method_cb(self):
        if self.color_bar is True:
            # Apply limits if any
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            if not isinstance(self.cb_vmin, type(None)) and isinstance(self.cb_vmax, type(None)):
                locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_nticks, endpoint=True)
            else:
                locator = ticker.MaxNLocator(nbins=self.cb_nticks)

            # Colorbar
            cbar = self.fig.colorbar(self.graph, spacing='proportional', ticks=locator, shrink=self.shrink,
                                     extend=self.extend, norm=None, orientation='vertical',
                                     ax=self.ax,
                                     format='%.' + str(self.tick_ndecimals) + 'f')

            # Ticks
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Title
            if not isinstance(self.cb_title, type(None)) and self.cb_y_title is False and self.cb_top_title is False:
                print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
            if self.cb_y_title is True:
                cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.yaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, size=self.cb_title_size,
                                                              weight=self.cb_title_weight)
                text.set_font_properties(font)
            if self.cb_top_title is True:
                cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                                  'horizontalalignment': 'left'},
                                  pad=self.cb_top_title_pad)
                cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                text = cbar.ax.title
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style, weight=self.cb_title_weight,
                                                              size=self.cb_title_size)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size)
            leg = self.ax.legend(loc=self.legend_loc, prop=legend_font,
                                 handleheight=self.legend_handleheight, ncol=self.legend_ncol)
            leg.legendHandles[0].set_color(cm.get_cmap(self.cmap)((np.clip(self.c.mean(), self.c.min(), self.c.max()) - self.c.min())/(self.c.max()-self.c.min())))

    def method_resize_axes(self):
        if self.resize_axes is True:
            if isinstance(self.x_upper_bound, type(None)):
                self.x_upper_bound = self.x.max()
            else:
                self.x_upper_resize_pad = 0
            if isinstance(self.x_lower_bound, type(None)):
                self.x_lower_bound = self.x.min()
            else:
                self.x_lower_resize_pad = 0

            if isinstance(self.y_upper_bound, type(None)):
                self.y_upper_bound = self.y.max()
            else:
                self.y_upper_resize_pad = 0
            if isinstance(self.y_lower_bound, type(None)):
                self.y_lower_bound = self.y.min()
            else:
                self.y_lower_resize_pad = 0

            if isinstance(self.x_upper_resize_pad, type(None)):
                self.x_upper_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.x_lower_resize_pad, type(None)):
                self.x_lower_resize_pad = 0.05*(self.x_upper_bound-self.x_lower_bound)
            if isinstance(self.y_upper_resize_pad, type(None)):
                self.y_upper_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)
            if isinstance(self.y_lower_resize_pad, type(None)):
                self.y_lower_resize_pad = 0.05*(self.y_upper_bound-self.y_lower_bound)

            if not isinstance(self.aspect, type(None)):
                self.ax.set_aspect(self.aspect)

            self.ax.set_xbound(lower=self.x_lower_bound - self.x_lower_resize_pad, upper=self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_lower_bound - self.y_lower_resize_pad, upper=self.y_upper_bound + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad, self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad, self.y_upper_bound + self.y_upper_resize_pad)

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
            self.ax.set_title(self.title, fontname=self.font, weight=weight,
                              color=self.workspace_color, size=self.title_size)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if not isinstance(self.x_label, type(None)):
            if self.x_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.x_label_size, labelpad=self.x_label_pad, rotation=self.x_label_rotation)
            if not isinstance(self.x_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.x_label_coords)

        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad, rotation=self.y_label_rotation)
            if not isinstance(self.y_label_coords, type(None)):
                self.ax.yaxis.set_label_coords(self.y_label_coords)

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
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if not isinstance(self.tick_color, type(None)):
            self.ax.tick_params(axis='both', color=self.tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color)
        #   Label size
        if not isinstance(self.tick_label_size_x, type(None)):
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x)
        if not isinstance(self.tick_label_size_y, type(None)):
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y)
        if not isinstance(self.tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=self.tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(self.x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(self.x_tick_labels[0] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[0],
                                           self.x_tick_labels[1] if not isinstance(self.x_tick_labels, type(None)) else self.ax.get_xlim()[1],
                                           self.x_tick_number))
        if not isinstance(self.y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(self.y_tick_labels[0] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[0],
                                           self.y_tick_labels[1] if not isinstance(self.y_tick_labels, type(None)) else self.ax.get_ylim()[1],
                                           self.y_tick_number))
        #   Prune
        if not isinstance(self.prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=self.prune))
        #   Float format
        float_format = '%.' + str(self.tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(self.custom_x_tick_labels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(self.custom_x_tick_labels[0],
                                                         self.custom_x_tick_labels[1],
                                                         self.x_tick_number),
                                             self.tick_ndecimals))
        if not isinstance(self.custom_y_tick_labels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(self.custom_y_tick_labels[0],
                                                         self.custom_y_tick_labels[1],
                                                         self.y_tick_number),
                                             self.tick_ndecimals))
        if self.date_tick_labels_x is True:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


def floating_text(ax, text, font, x, y, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, text, size=size, weight=weight, fontdict=font)
