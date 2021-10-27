import re
import inspect
import warnings
import numpy as np
import pandas as pd
import datetime as dt
from importlib import import_module

import matplotlib as mpl
from matplotlib import cm
from matplotlib import font_manager as font_manager
from matplotlib.ticker import FormatStrFormatter

from alexandria.shell import print_color
from alexandria.data_structs.array import span, ensure_ndarray

from mpl_plotter.two_d.mock import MockData


# NumPy ufunc size changed warning override -
# https://stackoverflow.com/questions/40845304/runtimewarning-numpy-dtype-size-changed-may-indicate-binary-incompatibility
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")


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
        self.plt.rcParams['font.sans-serif'] = "DejaVu Serif" if self.font == "serif" else self.font
        mpl.rc('font', cursive="Apple Chancery" if self.font == "serif" else self.font)
        mpl.rc('font', fantasy="Chicago" if self.font == "serif" else self.font)
        mpl.rc('font', monospace="Bitstream Vera Sans Mono" if self.font == "serif" else self.font)

        mpl.rc('mathtext', fontset=self.math_font)
        mpl.rc('text', color=self.font_color)

    def method_setup(self):
        if isinstance(self.fig, type(None)):
            if not self.plt.get_fignums():
                self.method_figure()
            else:
                self.fig = self.plt.gcf()
                self.ax = self.plt.gca()

        if isinstance(self.ax, type(None)):
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

    def method_figure(self):
        if self.style is not None:
            self.plt.style.use(self.style)
        self.fig = self.plt.figure(figsize=self.figsize)

    def method_grid(self):
        if self.grid:
            self.ax.grid(linestyle=self.grid_lines, color=self.grid_color)


class attributes:

    def method_background_color(self):
        self.fig.patch.set_facecolor(self.background_color_figure)
        self.ax.set_facecolor(self.background_color_plot)
        self.ax.patch.set_alpha(self.background_alpha)

    def method_workspace_style(self):
        if self.light:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193/256, 193/256, 193/256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2
            self.style = 'classic'
        elif self.dark:
            self.workspace_color = 'white' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (89/256, 89/256, 89/256) if isinstance(self.workspace_color2,
                                                                                 type(
                                                                                     None)) else self.workspace_color2
            self.style = 'dark_background'
        else:
            self.workspace_color = 'black' if isinstance(self.workspace_color, type(None)) else self.workspace_color
            self.workspace_color2 = (193/256, 193/256, 193/256) if isinstance(self.workspace_color2, type(
                None)) else self.workspace_color2

    def method_cb(self):
        pass
        if self.color_bar:
            if isinstance(self.norm, type(None)):
                return print_color("No norm selected for colorbar. Set norm=<parameter of choice>", "black")

            # Obtain and apply limits
            if isinstance(self.cb_vmin, type(None)):
                self.cb_vmin = self.norm.min()
            if isinstance(self.cb_vmax, type(None)):
                self.cb_vmax = self.norm.max()
            self.graph.set_clim([self.cb_vmin, self.cb_vmax])

            # Normalization
            locator = np.linspace(self.cb_vmin, self.cb_vmax, self.cb_tick_number)

            # Colorbar
            cb_decimals = self.tick_ndecimals if isinstance(self.cb_tick_ndecimals, type(None)) \
                else self.cb_tick_ndecimals
            cbar = self.fig.colorbar(self.graph,
                                     ax=self.ax,
                                     orientation=self.cb_orientation, shrink=self.shrink,
                                     ticks=locator,
                                     boundaries=locator if self.cb_hard_bounds else None,
                                     spacing='proportional',
                                     extend=self.extend,
                                     format='%.' + str(cb_decimals) + 'f',
                                     pad=self.cb_pad,
                                     )

            # Ticks
            #   Locator
            cbar.locator = locator
            #   Direction
            cbar.ax.tick_params(axis='y', direction='out')
            #   Tick label pad and size
            cbar.ax.yaxis.set_tick_params(pad=self.cb_axis_labelpad, labelsize=self.cb_ticklabelsize)

            # Colorbar title
            if self.cb_orientation == 'vertical':
                if self.cb_title is not None and not self.cb_y_title and not self.cb_top_title:
                    print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
                if self.cb_y_title:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_ytitle_labelpad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size + self.font_size_increase,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                if self.cb_top_title:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_top_title_pad)
                    cbar.ax.title.set_position((self.x_cb_top_title, self.cb_top_title_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title + self.font_size_increase)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_ytitle_labelpad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size + self.font_size_increase,
                                                       weight=self.cb_title_weight)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_legend(self):
        if self.legend:
            lines_labels = [ax.get_legend_handles_labels() for ax in self.fig.axes]
            lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size + self.font_size_increase)
            self.legend = self.fig.legend(lines, labels,
                                          loc=self.legend_loc,
                                          bbox_to_anchor=self.legend_bbox_to_anchor, prop=legend_font,
                                          handleheight=self.legend_handleheight, ncol=self.legend_ncol)

    def method_resize_axes(self):

        # Bound definition
        if self.x_bounds is not None:
            if self.x_bounds[0] is not None:
                self.x_lower_bound = self.x_bounds[0]
            if self.x_bounds[1] is not None:
                self.x_upper_bound = self.x_bounds[1]
        if self.y_bounds is not None:
            if self.y_bounds[0] is not None:
                self.y_lower_bound = self.y_bounds[0]
            if self.y_bounds[1] is not None:
                self.y_upper_bound = self.y_bounds[1]

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

            # Room to breathe
            if self.demo_pad_plot:
                pad_x = 0.05 * (abs(self.x + self.x.min()).max() - abs(self.x + self.x.min()).min())
                self.x_upper_resize_pad = pad_x
                self.x_lower_resize_pad = pad_x
                pad_y = 0.05 * (abs(self.y + self.y.min()).max() - abs(self.y + self.y.min()).min())
                self.y_upper_resize_pad = pad_y
                self.y_lower_resize_pad = pad_y

            # Allow constant input and single coordinate plots
            # Single coordinate plots
            if span(self.x_bounds) == 0 and span(self.y_bounds) == 0:
                # x bounds
                self.x_bounds = [self.x - self.x/2, self.x + self.x/2]
                self.x_upper_resize_pad = 0
                self.x_lower_resize_pad = 0
                # y bounds
                self.y_bounds = [self.y - self.y/2, self.y + self.y/2]
                self.y_upper_resize_pad = 0
                self.y_lower_resize_pad = 0
            # Constant x coordinate plot
            elif span(self.x_bounds) == 0:
                self.x_bounds = [self.x[0] - span(self.y)/2, self.x[0] + span(self.y)/2]
                self.x_upper_resize_pad = self.y_upper_resize_pad
                self.x_lower_resize_pad = self.y_lower_resize_pad
            # Constant y coordinate plot
            elif span(self.y_bounds) == 0:
                self.y_bounds = [self.y[0] - span(self.x)/2, self.y[0] + span(self.x)/2]
                self.y_upper_resize_pad = self.x_upper_resize_pad
                self.y_lower_resize_pad = self.x_lower_resize_pad

            # Set bounds
            self.ax.set_xbound(lower=self.x_bounds[0] - self.x_lower_resize_pad,
                               upper=self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ybound(lower=self.y_bounds[0] - self.y_lower_resize_pad,
                               upper=self.y_bounds[1] + self.y_upper_resize_pad)

            self.ax.set_xlim(self.x_bounds[0] - self.x_lower_resize_pad,
                             self.x_bounds[1] + self.x_upper_resize_pad)
            self.ax.set_ylim(self.y_bounds[0] - self.y_lower_resize_pad,
                             self.y_bounds[1] + self.y_upper_resize_pad)

            # Aspect ratio
            if self.aspect is not None and span(self.x_bounds) != 0 and span(self.y_bounds) != 0:
                y_range = span(self.y_bounds)
                x_range = span(self.x_bounds)

                aspect = x_range/y_range * self.aspect

                self.ax.set_aspect(aspect)

            # Scale
            if self.scale is not None:
                self.ax.set_aspect(self.scale)

    def method_title(self):
        if self.title is not None:
            self.ax.set_title(self.title,
                              fontname=self.font if isinstance(self.title_font, type(None)) else self.title_font,
                              weight=self.title_weight,
                              color=self.title_color if self.title_color is not None
                                    else self.font_color if self.font_color is not None
                                    else self.workspace_color,
                              size=self.title_size + self.font_size_increase)
            self.ax.title.set_position((0.5, self.title_y))

    def method_axis_labels(self):
        if self.x_label is not None:

            # Draw label
            self.ax.set_xlabel(self.x_label, fontname=self.font, weight=self.x_label_weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.x_label_size + self.font_size_increase, labelpad=self.x_label_pad,
                               rotation=self.x_label_rotation)

            # Custom coordinates if provided
            if self.x_label_coords is not None:
                self.ax.xaxis.set_label_coords(x=self.x_label_coords[0], y=self.x_label_coords[1])

        if self.y_label is not None:

            # y axis label rotation
            if isinstance(self.y_label_rotation, type(None)):
                latex_chars  = re.findall(r'\$\\(.*?)\$', self.y_label)
                label_length = len(self.y_label) - 2*len(latex_chars) - len(''.join(latex_chars).replace('//', '/'))
                self.y_label_rotation = 90 if label_length > 3 else 0

            # Draw label
            self.ax.set_ylabel(self.y_label, fontname=self.font, weight=self.y_label_weight,
                               color=self.workspace_color if self.font_color == self.workspace_color else self.font_color,
                               size=self.y_label_size + self.font_size_increase, labelpad=self.y_label_pad,
                               rotation=self.y_label_rotation)

            # Custom coordinates if provided
            if self.y_label_coords is not None:
                self.ax.yaxis.set_label_coords(x=self.y_label_coords[0], y=self.y_label_coords[1])

    def method_spines(self):
        for spine in self.ax.spines.values():
            spine.set_color(self.workspace_color if isinstance(self.spine_color, type(None)) else self.spine_color)

        if self.spines_removed is not None:
            for i in range(len(self.spines_removed)):
                if self.spines_removed[i] == 1:
                    self.ax.spines[["left", "bottom", "top", "right"][i]].set_visible(False)

        # Axis ticks
        left, bottom, top, right = self.ticks_where
        # Tick labels
        labelleft, labelbottom, labeltop, labelright = self.tick_labels_where

        self.ax.tick_params(axis='both', which='both',
                            top=top, right=right, left=left, bottom=bottom,
                            labeltop=labeltop, labelright=labelright, labelleft=labelleft, labelbottom=labelbottom)

    def method_ticks(self):
        """
        Defaults
        """
        # Fine tick locations
        if self.y is not None:  # Avoid issues with arrays with span 0 (vertical or horizontal lines)
            if span(self.y) == 0:
                self.fine_tick_locations = False
        if self.x is not None and self.y is not None:
            if self.fine_tick_locations and self.x.size != 0 and self.y.size != 0:
                if isinstance(self.x_custom_tick_locations, type(None)):
                    self.x_custom_tick_locations = [self.x.min(), self.x.max()]
                if isinstance(self.y_custom_tick_locations, type(None)):
                    self.y_custom_tick_locations = [self.y.min(), self.y.max()]
        """
        Checks
        """
        # Custom tick labels
        if self.x_custom_tick_labels is not None:                           # Ensure the number of ticks equals the
            if self.x_tick_number != len(self.x_custom_tick_labels):        # length of the list of custom tick
                self.x_tick_number = len(self.x_custom_tick_labels)         # labels.
        """
        Implementation
        """

        # Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')

        # Color
        if self.tick_color is not None:
            self.ax.tick_params(axis='both', color=self.tick_color)

        # Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)

        # Label size
        if self.x_tick_label_size is not None:
            self.ax.tick_params(axis='x', labelsize=self.x_tick_label_size + self.font_size_increase)
        elif self.tick_label_size is not None:
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size + self.font_size_increase)
        if self.y_tick_label_size is not None:
            self.ax.tick_params(axis='y', labelsize=self.y_tick_label_size + self.font_size_increase)
        elif self.tick_label_size is not None:
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size + self.font_size_increase)

        # Tick locations
        if isinstance(self.x_custom_tick_locations, type(None)):
            # No custom tick locations (none provided, fine_tick_locations=False)
            #   Control over tick number
            if self.x_tick_number > 1:
                ticklocs = np.linspace(*self.x_bounds, self.x_tick_number)
            else:
                ticklocs = np.array([self.x.mean()])
            self.ax.set_xticks(ticklocs)
        else:
            # Custom tick locations
            high = self.x_custom_tick_locations[0]
            low  = self.x_custom_tick_locations[1]
            # Set usual ticks
            if self.x_tick_number > 1:
                ticklocs = np.linspace(low, high, self.x_tick_number)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_xticks(ticklocs)
        if isinstance(self.y_custom_tick_locations, type(None)):
            # No custom tick locations (none provided, fine_tick_locations=False)
            #   Control over tick number
            if self.y_tick_number > 1:
                ticklocs = np.linspace(*self.y_bounds, self.y_tick_number)
            else:
                ticklocs = np.array([self.y.mean()])
            self.ax.set_yticks(ticklocs)
        else:
            # Custom tick locations
            high = self.y_custom_tick_locations[0]
            low  = self.y_custom_tick_locations[1]
            # Set usual ticks
            if self.y_tick_number > 1:
                ticklocs = np.linspace(low, high, self.y_tick_number)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_yticks(ticklocs)

        # Float format
        x_decimals = self.tick_ndecimals if isinstance(self.x_tick_ndecimals, type(None)) \
            else self.x_tick_ndecimals
        y_decimals = self.tick_ndecimals if isinstance(self.y_tick_ndecimals, type(None)) \
            else self.y_tick_ndecimals
        float_format_x = '%.' + str(x_decimals) + 'f'
        float_format_y = '%.' + str(y_decimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format_x))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format_y))

        # Custom tick labels
        if self.x_custom_tick_labels is not None:
            if len(self.x_custom_tick_labels) == 2 and len(self.x_custom_tick_labels) != self.x_tick_number:
                self.x_custom_tick_labels = np.linspace(self.x_custom_tick_labels[0],
                                                        self.x_custom_tick_labels[1],
                                                        self.x_tick_number)
            self.ax.set_xticklabels(self.x_custom_tick_labels[::-1])
        if self.y_custom_tick_labels is not None:
            if len(self.y_custom_tick_labels) == 2 and len(self.y_custom_tick_labels) != self.y_tick_number:
                self.y_custom_tick_labels = np.linspace(self.y_custom_tick_labels[0],
                                                        self.y_custom_tick_labels[1],
                                                        self.y_tick_number)
            self.ax.set_yticklabels(self.y_custom_tick_labels[::-1])

        # Date tick labels
        if self.x_date_tick_labels:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.x_tick_number)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        # Tick-label pad
        if self.tick_label_pad is not None:
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)

        # Rotation
        if self.x_tick_rotation is not None:
            self.ax.tick_params(axis='x', rotation=self.x_tick_rotation)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if self.y_tick_rotation is not None:
            self.ax.tick_params(axis='y', rotation=self.y_tick_rotation)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")


class plot(canvas, attributes):

    def init(self):

        self.method_backend()

        self.plt = import_module("matplotlib.pyplot")

        """
        Run
        """

        self.run()

    def run(self):
        self.main()
        self.finish()

    def main(self):
        # Canvas setup
        self.method_fonts()
        self.method_setup()
        self.method_grid()
        self.method_background_color()
        self.method_workspace_style()

        # Mock plot
        self.mock()
        # Plot
        self.plot()

    def finish(self):
        # Resize axes
        self.method_resize_axes()
        # Legend
        self.method_legend()
        # Colorbar
        self.method_cb()

        # Makeup
        self.method_title()
        self.method_axis_labels()
        self.method_spines()
        self.method_ticks()

        # Save
        self.method_save()

        self.method_show()

    def method_save(self):
        if self.filename:
            self.plt.savefig(self.filename, dpi=self.dpi)

    def method_show(self):
        if self.show:
            self.fig.tight_layout()
            self.plt.show()
        else:
            if not self.suppress:
                print('Ready for next subplot')


class line(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, line_width=2,
                 # Specifics: color
                 color='darkred', cmap='RdBu_r', alpha=None, norm=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Line plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param line_width: Line width

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None

        self.init()

    def plot(self):

        if isinstance(self.norm, type(None)):
            self.graph = self.ax.plot(self.x, self.y, label=self.plot_label, linewidth=self.line_width,
                                      color=self.color,
                                      zorder=self.zorder,
                                      alpha=self.alpha,
                                      )[0]
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

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()
            if self.norm:
                self.norm = self.y


class scatter(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, point_size=5, marker='o', facecolors=None,
                 # Specifics: color
                 color="C0", cmap='RdBu_r', alpha=None, norm=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Scatter plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param point_size: Point size
        :param marker: Dot marker

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None

        self.init()

    def plot(self):

        if self.norm is not None:
            self.graph = self.ax.scatter(self.x, self.y, label=self.plot_label,
                                         s=self.point_size, marker=self.marker, facecolors=self.facecolors,
                                         c=self.norm, cmap=self.cmap,
                                         zorder=self.zorder,
                                         alpha=self.alpha)
        else:
            self.graph = self.ax.scatter(self.x, self.y, label=self.plot_label,
                                         s=self.point_size, marker=self.marker, facecolors=self.facecolors,
                                         color=self.color,
                                         zorder=self.zorder,
                                         alpha=self.alpha)

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y = MockData().spirograph()
            self.norm = self.y


class heatmap(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, normvariant='SymLog',
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Heatmap plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param z: z
        :param normvariant: Detailed information in the Matplotlib documentation

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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
        # T
        # urn all instance arguments to instance attributes
        for item in inspect.signature(heatmap).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.z = ensure_ndarray(self.z) if self.z is not None else None

        self.init()

    def plot(self):
        self.graph = self.ax.pcolormesh(self.x, self.y, self.z, cmap=self.cmap,
                                        zorder=self.zorder,
                                        alpha=self.alpha,
                                        label=self.plot_label,
                                        shading='auto'
                                        )
        # Resize axes
        self.method_resize_axes()

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x, self.y, self.z = MockData().waterdrop()


class quiver(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None,
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 rule=None, custom_rule=None, vector_width=0.01, vector_min_shaft=2, vector_length_threshold=0.1,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Quiver plot class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param u: u
        :param v: v
        :param rule:  lambda function of u and v
            rule = lambda u, v: (u**2+v**2)
        :param custom_rule: Array assigning a color to each (x, y, u, v) vector
        :param vector_width: Vector width
        :param vector_min_shaft: Minimum vector shaft
        :param vector_length_threshold: Minimum vector length

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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
        # T
        # urn all instance arguments to instance attributes
        for item in inspect.signature(quiver).parameters:
            setattr(self, item, eval(item))


        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.init()

    def plot(self):

        # Color rule
        self.method_rule()

        self.graph = self.ax.quiver(self.x, self.y, self.u, self.v,
                                    color=self.color, cmap=self.cmap,
                                    width=self.vector_width,
                                    minshaft=self.vector_min_shaft,
                                    minlength=self.vector_length_threshold,
                                    label=self.plot_label,
                                    zorder=self.zorder,
                                    alpha=self.alpha
                                    )

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.random.random(100)
            self.y = np.random.random(100)
            self.u = np.random.random(100)
            self.v = np.random.random(100)
            self.norm = np.sqrt(self.u ** 2 + self.v ** 2)

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
        c = (c.ravel() - c.min())/c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(self.cmap)
        self.color = cmap(c)


class streamline(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, u=None, v=None, line_width=1, line_density=2,
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):
        """
        Streamline class
        mpl_plotter - 2D

        Specifics
        :param x: x
        :param y: y
        :param u: u
        :param v: v
        :param line_width: Streamline width
        :param line_density: Measure of the amount of streamlines displayed. Low value (default=2)


        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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
        for item in inspect.signature(streamline).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.u = ensure_ndarray(self.u) if self.u is not None else None
        self.v = ensure_ndarray(self.v) if self.v is not None else None

        self.init()

    def plot(self):

        # Color rule
        self.method_rule()

        # Plot
        self.graph = self.ax.streamplot(self.x, self.y, self.u, self.v,
                                        color=self.color,
                                        cmap=self.cmap,
                                        linewidth=self.line_width,
                                        density=self.line_density,
                                        zorder=self.zorder,
                                        ).lines

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.linspace(0, 10, 100)
            self.y = np.linspace(0, 10, 100)
            self.x, self.y = np.meshgrid(self.x, self.y)
            self.u = np.cos(self.x)
            self.v = np.cos(self.y)
            self.color = self.u

    def method_rule(self):
        if isinstance(self.color, type(None)):
            rule_color = lambda u: np.sqrt(self.u ** 2 + self.v ** 2) / np.sqrt(self.u.max() ** 2 + self.v.max() ** 2)
            self.color = rule_color(self.u)


class fill_area(plot):

    def __init__(self,
                 # Specifics
                 x=None, y=None, z=None, between=False, below=False, above=False,
                 # Specifics: color
                 color=None, cmap='RdBu_r', alpha=None, norm=None,
                 # Backend
                 backend='Qt5Agg',
                 # Fonts
                 font='serif', math_font="dejavuserif", font_color="black", font_size_increase=0,
                 # Figure, axes
                 fig=None, ax=None, figsize=None, shape_and_position=111, resize_axes=True,
                 scale=None, aspect=1,
                 # Setup
                 workspace_color=None, workspace_color2=None,
                 background_color_figure='white', background_color_plot='white', background_alpha=1,
                 style=None, light=None, dark=None,
                 # Spines
                 spine_color=None, spines_removed=(0, 0, 1, 1),
                 # Bounds
                 x_upper_bound=None, x_lower_bound=None,
                 y_upper_bound=None, y_lower_bound=None,
                 x_bounds=None, y_bounds=None,
                 # Pads
                 demo_pad_plot=False,
                 x_upper_resize_pad=0, x_lower_resize_pad=0,
                 y_upper_resize_pad=0, y_lower_resize_pad=0,
                 # Grid
                 grid=True, grid_color='lightgrey', grid_lines='-.',
                 # Title
                 title=None, title_size=12, title_y=1.025, title_weight=None, title_font=None, title_color=None,
                 # Labels
                 x_label=None, x_label_size=12, x_label_pad=10, x_label_rotation=None, x_label_weight=None,
                 y_label=None, y_label_size=12, y_label_pad=10, y_label_rotation=None, y_label_weight=None,
                 # Ticks
                 x_tick_number=5,
                 y_tick_number=5,
                 x_label_coords=None, y_label_coords=None,
                 tick_color=None, tick_label_pad=5,
                 ticks_where=(1, 1, 0, 0),
                 # Tick labels
                 tick_label_size=10, x_tick_label_size=None, y_tick_label_size=None,
                 x_custom_tick_locations=None, y_custom_tick_locations=None, fine_tick_locations=True,
                 x_custom_tick_labels=None, y_custom_tick_labels=None,
                 x_date_tick_labels=False, date_format='%Y-%m-%d',
                 tick_ndecimals=1, x_tick_ndecimals=None, y_tick_ndecimals=None,
                 x_tick_rotation=None, y_tick_rotation=None,
                 tick_labels_where=(1, 1, 0, 0),
                 # Color bar
                 color_bar=False, cb_pad=0.2, cb_axis_labelpad=10, shrink=0.75, extend='neither',
                 cb_title=None, cb_orientation='vertical',
                 cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                 cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                 cb_y_title=False, cb_top_title_pad=None, x_cb_top_title=0,
                 cb_vmin=None, cb_vmax=None, cb_hard_bounds=False, cb_outline_width=None,
                 cb_tick_number=5, cb_ticklabelsize=10, cb_tick_ndecimals=None,
                 # Legend
                 plot_label=None,
                 legend=False, legend_loc='upper right', legend_bbox_to_anchor=None,
                 legend_size=13, legend_weight='normal',
                 legend_style='normal', legend_handleheight=None, legend_ncol=1,
                 # Subplots
                 show=False, zorder=None,
                 # Save
                 filename=None, dpi=None,
                 # Suppress output
                 suppress=True
                 ):

        """
        Fill area class
        mpl_plotter - 2D

        Specifics
        :param x: Horizontal axis values
        :param y: Curve 1
        :param z: Curve 2

        The following parameters can be used in combination:

        :param between: Fill between Curve 1 and Curve 2
        :param below: Fill below Curve 1 and Curve 2
        :param above: Fill above Curve 1 and Curve 2

        Color:
        :param color: Solid color
        :param cmap: Colormap
        :param alpha: Alpha
        :param norm: Norm to assign colormap values

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
        for item in inspect.signature(fill_area).parameters:
            setattr(self, item, eval(item))

        # Ensure x and y are NumPy arrays
        self.x = ensure_ndarray(self.x) if self.x is not None else None
        self.y = ensure_ndarray(self.y) if self.y is not None else None
        self.z = ensure_ndarray(self.z) if self.z is not None else None

        self.init()

    def plot(self):

        """
        Fill the region below the intersection of S and Z
        """
        if self.z is not None:
            if self.between:
                self.ax.fill_between(self.x, self.y, self.z, facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if self.below:
                self.ax.fill_between(self.x, self.i_below(), np.zeros(self.y.shape), facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if self.above:
                self.ax.fill_between(self.x, self.i_above(), np.zeros(self.y.shape), facecolor=self.color,
                                     alpha=self.alpha, label=self.plot_label)
            if not self.between and not self.below and not self.above:
                print_color('No area chosen to fill: specify whether to fill "between", "below" or "above" the curves',
                            'grey')
        else:
            self.ax.fill_between(self.x, self.y, np.zeros(self.y.shape), facecolor=self.color, alpha=self.alpha)

    def i_below(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] <= self.z[i] else self.z[i]
        return c

    def i_above(self):
        # Curve
        c = np.zeros(self.y.shape, dtype=float)
        for i in range(len(c)):
            c[i] = self.y[i] if self.y[i] >= self.z[i] else self.z[i]
        return c

    def intersection(self):
        return np.nonzero(np.absolute(self.y - self.z) == min(np.absolute(self.y - self.z)))[0]

    def mock(self):
        if isinstance(self.x, type(None)) and isinstance(self.y, type(None)):
            self.x = np.arange(-6, 6, .01)
            self.y = MockData().boltzman(self.x, 0, 1)
            self.z = 1 - MockData().boltzman(self.x, 0.5, 1)
            line(x=self.x, y=self.y,
                 grid=False, resize_axes=False)
            line(x=self.x, y=self.z,
                 grid=False, resize_axes=False)
            self.below = True


def floating_text(ax, text, font="serif", x=0.5, y=0.5, size=20, weight='normal', color='darkred'):
    # Font
    font = {'family': font,
            'color': color,
            'weight': weight,
            'size': size,
            }
    # Floating text
    ax.text(x, y, text, size=size, weight=weight, fontdict=font)
