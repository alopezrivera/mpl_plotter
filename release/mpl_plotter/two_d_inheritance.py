import inspect
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib as mpl

from importlib import import_module

from matplotlib import cm
from matplotlib import font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.resources.mock_data import MockData
from mpl_plotter.resources.functions import normalize
from mpl_plotter.resources.functions import print_color

# from matplotlib import rc
# from matplotlib import colors
# from matplotlib import dates as mdates
# from numpy import sin, cos
# from skimage import measure
# from matplotlib import ticker
# from pylab import floor


class plot:

    def method_figure(self):
        if not isinstance(self.style, type(None)):
            self.plt.style.use(self.style)
        self.fig = self.plt.figure(figsize=self.figsize)

    def method_style(self):
        if self.light:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89 / 256, 89 / 256, 89 / 256) if isinstance(self.workspace_color2,
                                                                                 type(
                                                                                     None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193 / 256, 193 / 256, 193 / 256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
        self.ax.set_facecolor(self.background_color_plot)
        self.fig.patch.set_facecolor(self.background_color_figure)

    def method_setup(self):
        if isinstance(self.fig, type(None)):
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                self.ax = self.plt.gca()

        if isinstance(self.ax, type(None)):
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_cb(self):
        if self.color_bar is True:
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

            self.ax.set_xlim(self.x_lower_bound - self.x_lower_resize_pad,
                             self.x_upper_bound + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_lower_bound - self.y_lower_resize_pad,
                             self.y_upper_bound + self.y_upper_resize_pad)

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.more_subplots_left is not True:
            self.fig.tight_layout()
            self.plt.show()
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
                bottom = False
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
            self.ax.xaxis.set_major_locator(self.plt.MaxNLocator(prune=self.prune))
        if not isinstance(self.prune, type(None)):
            self.ax.yaxis.set_major_locator(self.plt.MaxNLocator(prune=self.prune))
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
            self.plt.grid(linestyle=self.grid_lines, color=self.grid_color)


class line(plot):

    def __init__(self,
                 # Specifics
                 line_width=3,
                 # Base
                 x=None, y=None,
                 backend='Qt5Agg', plot_label='Plot', font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None, spines_removed=('top', 'right'),
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, alpha=None, norm=None, cmap='RdBu_r',
                 # Title
                 title='Title', title_bold=False, title_size=12, title_y=1.025,
                 # Labels
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 ):
        """
        @param line_width:
        @param x:
        @param y:
        @param backend: Interactive plotting backends. Working with Python 3.7.6: Qt5Agg, QT4Agg, TkAgg.
                                Backend error:
                                    pip install pyqt5
                                    pip install tkinter
                                    pip install tk
                                    ... stackoverflow
                                Plotting window freezes even if trying different backends with no backend error: python configuration problem
                                    backend=None
        @param plot_label:
        @param font:
        @param fig:
        @param ax:
        @param figsize:
        @param shape_and_position:
        @param prune:
        @param resize_axes:
        @param aspect:
        @param spines_removed:
        @param workspace_color:
        @param workspace_color2:
        @param background_color_figure:
        @param background_color_plot:
        @param style:
        @param light:
        @param dark:
        @param x_upper_bound:
        @param x_lower_bound:
        @param y_upper_bound:
        @param y_lower_bound:
        @param x_bounds:
        @param y_bounds:
        @param x_upper_resize_pad:
        @param x_lower_resize_pad:
        @param y_upper_resize_pad:
        @param y_lower_resize_pad:
        @param grid:
        @param grid_color:
        @param grid_lines:
        @param color:
        @param alpha:
        @param norm:
        @param cmap:
        @param title:
        @param title_bold:
        @param title_size:
        @param title_y:
        @param x_label:
        @param x_label_bold:
        @param x_label_size:
        @param x_label_pad:
        @param x_label_rotation:
        @param y_label:
        @param y_label_bold:
        @param y_label_size:
        @param y_label_pad:
        @param y_label_rotation:
        @param x_tick_number:
        @param x_tick_labels:
        @param y_tick_number:
        @param y_tick_labels:
        @param x_tick_rotation:
        @param y_tick_rotation:
        @param x_label_coords:
        @param y_label_coords:
        @param tick_color:
        @param tick_label_pad:
        @param tick_ndecimals:
        @param tick_label_size:
        @param tick_label_size_x:
        @param tick_label_size_y:
        @param custom_x_tick_labels:
        @param custom_y_tick_labels:
        @param date_tick_labels_x:
        @param date_format:
        @param color_bar:
        @param cb_pad:
        @param extend:
        @param cb_title:
        @param cb_orientation:
        @param cb_axis_labelpad:
        @param cb_tick_number:
        @param shrink:
        @param cb_outline_width:
        @param cb_title_rotation:
        @param cb_title_style:
        @param cb_title_size:
        @param cb_top_title_y:
        @param cb_ytitle_labelpad:
        @param cb_title_weight:
        @param cb_top_title:
        @param cb_y_title:
        @param cb_top_title_pad:
        @param cb_top_title_x:
        @param cb_vmin:
        @param cb_vmax:
        @param cb_ticklabelsize:
        @param cb_hard_bounds:
        @param legend:
        @param legend_loc:
        @param legend_size:
        @param legend_weight:
        @param legend_style:
        @param legend_handleheight:
        @param legend_ncol:
        @param more_subplots_left:
        @param zorder:
        @param filename:
        @param dpi:
        """

        if not isinstance(backend, type(None)):
            try:
                mpl.use(backend)
            except AttributeError:
                raise AttributeError('{} backend not supported with current Python configuration'.format(backend))

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

        self.plt = import_module("matplotlib.pyplot")

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(line).parameters:
            setattr(self, item, eval(item))

        """
        Run
        """

        self.run()

    def run(self):

        self.method_setup()

        self.method_style()

        # Mock plot
        self.mock_line()

        # Main
        self.main()

        # Colorbar
        self.method_cb()

        # Legend
        self.method_legend()

        # # Resize axes
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

    def main(self):

        if isinstance(self.norm, type(None)):
            self.graph = self.ax.plot(self.x, self.y, label=self.plot_label, linewidth=self.line_width, color=self.color,
                                      zorder=self.zorder,
                                      alpha=self.alpha,
                                      )
        else:
            # Create a set of line segments so that we can color them individually
            # This creates the points as a N x 1 x 2 array so that we can stack points
            # together easily to get the segments. The segments array for line collection
            # needs to be (numlines) x (points per line) x 2 (for x and y)
            points = np.array([self.x, self.y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            # Create a continuous norm to map from data points to colors
            _norm = self.norm(self.x) if hasattr(self.norm, '__call__') else self.norm
            norm = self.plt.Normalize(_norm.min(), _norm.max())
            lc = mpl.collections.LineCollection(segments, cmap=self.cmap, norm=norm)

            # Set the values used for colormapping
            lc.set_array(self.norm)
            lc.set_linewidth(self.line_width)
            self.graph = self.ax.add_collection(lc)

    def mock_line(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()


class scatter(plot):
    pass


class heatmap(plot):
    pass


class quiver(plot):
    pass


class streamline(plot):
    pass


class fill_area(plot):

    def __init__(self,
                 # Specifics
                 z=None,
                 # Base
                 x=None, y=None,
                 backend='Qt5Agg', plot_label='Plot', font='serif',
                 # Figure, axis
                 fig=None, ax=None, figsize=None, shape_and_position=111,
                 # Setup
                 prune=None, resize_axes=True, aspect=None, spines_removed=('top', 'right'),
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white',
                 style=None, light=None, dark=None,
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 x_upper_resize_pad=None, x_lower_resize_pad=None,
                 y_upper_resize_pad=None, y_lower_resize_pad=None,
                 # Grid
                 grid=False, grid_color='black', grid_lines='-.',
                 # Color
                 color=None, alpha=None, norm=None, cmap='RdBu_r',
                 # Title
                 title='Title', title_bold=False, title_size=12, title_y=1.025,
                 # Labels
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 # Ticks
                 x_tick_number=5, x_tick_labels=None,
                 y_tick_number=5, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None, x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                 # Tick labels
                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False, date_format='%Y-%m-%d',
                 # Color bar
                 color_bar=False, cb_pad=0.2, extend='neither',
                 cb_title=None, cb_orientation='vertical', cb_axis_labelpad=10, cb_tick_number=5, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None,
                 cb_ticklabelsize=10, cb_hard_bounds=False,
                 # Legend
                 legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 more_subplots_left=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
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
        :param cb_tick_number:
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

        # matplotlib.use() must be called *before* pylab, matplotlib.pyplot,
        # or matplotlib.backends is imported for the first time.

        self.plt = import_module("matplotlib.pyplot")

        # Turn all instance arguments to instance attributes
        for item in inspect.signature(fill_area).parameters:
            setattr(self, item, eval(item))

        """
        Run
        """

        self.run()

    def main(self):

        """
        Fill the region below the intersection of S and Z
        """
        self.ax.fill(self.x, self.intersection() if not isinstance(self.z, type(None)) else self.y,
                     facecolor=self.color, alpha=self.alpha)

    def run(self):

        self.method_setup()

        self.method_style()

        # Mock plot
        self.mock_fill()

        """
        Main
        """
        self.main()

        # Colorbar
        self.method_cb()

        # Legend
        self.method_legend()

        # # Resize axes
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

    def intersection(self):
        # Intersection index
        idx = np.nonzero(np.absolute(self.y - self.z) == min(np.absolute(self.y - self.z)))[0][0]
        # Curve
        c = np.zeros(self.y.shape, dtype=np.float)
        c[:idx] = self.y[:idx]  # Y is S up to the intersection
        c[idx:] = self.z[idx:]  # and Z beyond it
        return c

    def mock_fill(self):

        from resources.mock_data import MockData

        self.x = np.arange(-6, 6, .01)
        self.y = MockData().boltzman(self.x, 0, 1)
        self.z = 1 - MockData().boltzman(self.x, 0.5, 1)
        line(x=self.x, y=self.y, color='darkred', more_subplots_left=True)
        line(x=self.x, y=self.z, color='darkred', more_subplots_left=True)




