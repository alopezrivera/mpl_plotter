import numpy as np
import matplotlib as mpl

from matplotlib import pyplot as plt
from matplotlib import rc
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource
from matplotlib.ticker import FormatStrFormatter
import matplotlib.font_manager as font_manager
import matplotlib.dates as mdates

from pylab import *

from numpy import sin, cos
from skimage import measure

from resources.mock_data import MockData
from resources.colormaps import ColorMaps


class quiver:

    def __init__(self,
                 x=None, y=None, u=None, v=None,
                 backend='Qt5Agg', fig=None, ax=None, figsize=None, shape_and_position=None,
                 font='serif', light=None, dark=None,
                 x_bounds=None, y_bounds=None, x_resize_pad=5, y_resize_pad=5,
                 color=None, workspace_color=None, workspace_color2=None,
                 rule=None, custom_rule=None, vector_width=0.01, vector_min_shaft=2, vector_length_threshold=0.1,
                 label='Plot', legend=False, legend_loc='upper right', legend_size=13, legend_weight='normal',
                 legend_style='normal',
                 grid=False, grid_color='black', grid_lines='-.', spines_removed=('top', 'right'),
                 cmap='RdBu_r', color_bar=False, extend='neither', cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                 cb_outline_width=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, cb_top_title_x=0, cb_vmin=None, cb_vmax=None, cb_ticklabelsize=10,
                 prune=None, resize_axes=True, aspect=1,
                 title='Quiver', title_bold=False, title_size=12, title_y=1.025,
                 x_label='x', x_label_bold=False, x_label_size=12, x_label_pad=5, x_label_rotation=None,
                 y_label='y', y_label_bold=False, y_label_size=12, y_label_pad=5, y_label_rotation=None,
                 x_tick_number=10, x_tick_labels=None,
                 y_tick_number=None, y_tick_labels=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_color=None, tick_label_pad=5, tick_ndecimals=1,

                 tick_label_size=None, tick_label_size_x=None, tick_label_size_y=None,
                 more_subplots_left=False,
                 filename=None, dpi=None,
                 custom_x_tick_labels=None, custom_y_tick_labels=None, date_tick_labels_x=False
                 ):

        try:
            mpl.use(backend)
        except:
            sys.exit('{} backend not supported with current Python configuration'.format(backend))

        # Specifics
        self.u = u
        self.v = v
        self.rule = rule
        self.custom_rule = custom_rule
        self.vector_width = vector_width
        self.vector_min_shaft = vector_min_shaft
        self.vector_length_threshold = vector_length_threshold

        # Base
        self.x = x
        self.y = y
        self.fig = fig
        self.ax = ax
        self.figsize = figsize
        self.shape_and_position = shape_and_position
        self.font = font
        self.light = light
        self.dark = dark
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.x_resize_pad = x_resize_pad
        self.y_resize_pad = y_resize_pad
        # Legend
        self.label = label
        self.legend = legend
        self.legend_loc = legend_loc
        self.legend_size = legend_size
        self.legend_weight = legend_weight
        self.legend_style = legend_style
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
        # Display and save
        self.more_subplots_left = more_subplots_left
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
                                    label=self.label
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

        if isinstance(self.fig, type(None)):
            self.method_figure()

        if isinstance(self.ax, type(None)):
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
            # Take limits from plot
            if isinstance(self.cb_vmin, type(None)) and isinstance(self.cb_vmax, type(None)):
                # Take limits from plot
                self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            if norm is None:
                locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_nticks, endpoint=True)
            else:
                locator = None

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
                font = matplotlib.font_manager.FontProperties(family=self.font, style=self.cb_title_style, size=self.cb_title_size,
                                                              weight=self.cb_title_weight)
                text.set_font_properties(font)
            if self.cb_top_title is True:
                cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                                  'horizontalalignment': 'left'},
                                  pad=self.cb_top_title_pad)
                cbar.ax.title.set_position((self.cb_top_title_x, self.cb_top_title_y))
                text = cbar.ax.title
                font = matplotlib.font_manager.FontProperties(family=self.font, style=self.cb_title_style, weight=self.cb_title_weight,
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
            leg = self.ax.legend(loc=self.legend_loc, prop=legend_font)
            leg.legendHandles[0].set_color(cm.get_cmap(self.cmap)((np.clip(self.c.mean(), self.c.min(), self.c.max()) - self.c.min())/(self.c.max()-self.c.min())))

    def method_resize_axes(self):
        if self.resize_axes is True:
            if isinstance(self.x_bounds, type(None)):
                self.x_bounds = [self.x.min(), self.x.max()]
            else:
                self.x_resize_pad = 0
            if isinstance(self.y_bounds, type(None)):
                self.y_bounds = [self.y.min(), self.y.max()]
            else:
                self.y_resize_pad = 0

            self.ax.set_aspect(self.aspect)
            self.ax.set_xbound(lower=self.x_bounds[0] - self.x_resize_pad, upper=self.x_bounds[1] + self.x_resize_pad)
            self.ax.set_ybound(lower=self.y_bounds[0] - self.y_resize_pad, upper=self.y_bounds[1] + self.y_resize_pad)

            self.ax.set_xlim(self.x_bounds[0] - self.x_resize_pad, self.x_bounds[1] + self.x_resize_pad)
            self.ax.set_ylim(self.y_bounds[0] - self.y_resize_pad, self.y_bounds[1] + self.y_resize_pad)

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
        if not isinstance(self.y_label, type(None)):
            if self.y_label_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=weight,
                               color=self.workspace_color, size=self.y_label_size, labelpad=self.y_label_pad, rotation=self.y_label_rotation)
            self.ax.yaxis.set_label_coords(-0.275, 0.425)

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
            fmtd = []
            for date in list(plt.xticks()[0]):
                date = '{}/{}'.format(int(floor(date)), int(12 * (date % 1))) if date % 1 > 0 else '{}'.format(int(floor(date)))
                fmtd.append(date)
            self.ax.set_xticklabels(fmtd)
        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if not isinstance(self.tick_label_pad, type(None)):
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)
        #   Rotation
        if not isinstance(self.x_tick_rotation, type(None)):
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
        if not isinstance(self.y_tick_rotation, type(None)):
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)

    def method_grid(self):
        if self.grid is not False:
            plt.grid(linestyle=self.grid_lines, color=self.grid_color)


def test():
    quiver(x_bounds=[0, 1], y_bounds=[0, 1])
