# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Guides
------
"""


import numpy as np
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.utils import span


class guides:

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
            cb_decimals = self.tick_label_decimals if isinstance(self.cb_tick_label_decimals, type(None)) \
                else self.cb_tick_label_decimals
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
                if self.cb_title is not None and not self.cb_title_side and not self.cb_title_top:
                    print('Input colorbar title location with booleans: cb_title_side=True or cb_title_top=True')
                if self.cb_title_side:
                    cbar.ax.set_ylabel(self.cb_title, rotation=self.cb_title_rotation,
                                       labelpad=self.cb_title_side_pad)
                    text = cbar.ax.yaxis.label
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           size=self.cb_title_size + self.font_size_increase,
                                                           weight=self.cb_title_weight)
                    text.set_font_properties(font)
                elif self.cb_title_top:
                    cbar.ax.set_title(self.cb_title, rotation=self.cb_title_rotation,
                                      fontdict={'verticalalignment': 'baseline',
                                                'horizontalalignment': 'left'},
                                      pad=self.cb_title_top_pad)
                    cbar.ax.title.set_position((self.cb_title_top_x, self.cb_title_top_y))
                    text = cbar.ax.title
                    font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                           weight=self.cb_title_weight,
                                                           size=self.cb_title_size + self.font_size_increase)
                    text.set_font_properties(font)
            elif self.cb_orientation == 'horizontal':
                cbar.ax.set_xlabel(self.cb_title, rotation=self.cb_title_rotation, labelpad=self.cb_title_side_pad)
                text = cbar.ax.xaxis.label
                font = mpl.font_manager.FontProperties(family=self.font, style=self.cb_title_style,
                                                       size=self.cb_title_size + self.font_size_increase,
                                                       weight=self.cb_title_weight)
                text.set_font_properties(font)

            # Outline
            cbar.outline.set_edgecolor(self.workspace_color2)
            cbar.outline.set_linewidth(self.cb_outline_width)

    def method_grid(self):
        if self.grid:
            self.ax.grid(linestyle=self.grid_lines, color=self.grid_color)

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

    def method_tick_locs(self):
        # ----------------
        # Input validation
        # ----------------
        if self.y is not None:  # Avoid issues with arrays with span 0 (vertical or horizontal lines)
            if span(self.y) == 0:
                self.tick_locations_fine = False
        if self.x is not None and self.y is not None:
            if self.tick_locations_fine and self.x.size != 0 and self.y.size != 0:
                if isinstance(self.tick_locations_x, type(None)):
                    self.tick_locations_x = [self.x.min(), self.x.max()]
                if isinstance(self.tick_locations_y, type(None)):
                    self.tick_locations_y = [self.y.min(), self.y.max()]
        # Ensure the number of ticks equals the length of the list of
        # tick labels, if provided
        if self.tick_labels_x is not None:                   
            if self.tick_number_x != len(self.tick_labels_x):
                self.tick_number_x = len(self.tick_labels_x) 
        if self.tick_labels_y is not None:
            if self.tick_number_y != len(self.tick_labels_y):        # length of the list of custom tick
                self.tick_number_y = len(self.tick_labels_y)         # labels.

        # ----------------
        #  Implementation
        # ----------------
        if isinstance(self.tick_locations_x, type(None)):
            # No custom tick locations (none provided, tick_locations_fine=False)
            #   Control over tick number
            if self.tick_number_x > 1:
                ticklocs = np.linspace(*self.bounds_x, self.tick_number_x)
            else:
                ticklocs = np.array([self.x.mean()])
            self.ax.set_xticks(ticklocs)
        else:
            # Custom tick locations
            high = self.tick_locations_x[0]
            low  = self.tick_locations_x[1]
            # Set usual ticks
            if self.tick_number_x > 1:
                ticklocs = np.linspace(low, high, self.tick_number_x)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_xticks(ticklocs)
        if isinstance(self.tick_locations_y, type(None)):
            # No custom tick locations (none provided, tick_locations_fine=False)
            #   Control over tick number
            if self.tick_number_y > 1:
                ticklocs = np.linspace(*self.bounds_y, self.tick_number_y)
            else:
                ticklocs = np.array([self.y.mean()])
            self.ax.set_yticks(ticklocs)
        else:
            # Custom tick locations
            high = self.tick_locations_y[0]
            low  = self.tick_locations_y[1]
            # Set usual ticks
            if self.tick_number_y > 1:
                ticklocs = np.linspace(low, high, self.tick_number_y)
            # Special case: single tick
            else:
                ticklocs = np.array([low + (high - low)/2])
            self.ax.set_yticks(ticklocs)

    def method_tick_labels(self):

        # Tick-axis pad
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')

        # Tick color
        if self.tick_color is not None:
            self.ax.tick_params(axis='both', color=self.tick_color)

        # Custom tick labels
        if self.tick_labels_x is not None:
            if len(self.tick_labels_x) == 2 and len(self.tick_labels_x) != self.tick_number_x:
                self.tick_labels_x = np.linspace(self.tick_labels_x[0],
                                                        self.tick_labels_x[1],
                                                        self.tick_number_x)
            self.ax.set_xticklabels(self.tick_labels_x[::-1])
        if self.tick_labels_y is not None:
            if len(self.tick_labels_y) == 2 and len(self.tick_labels_y) != self.tick_number_y:
                self.tick_labels_y = np.linspace(self.tick_labels_y[0],
                                                        self.tick_labels_y[1],
                                                        self.tick_number_y)
            self.ax.set_yticklabels(self.tick_labels_y[::-1])

        # Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.workspace_color if self.font_color == self.workspace_color else self.font_color)

        # Label size
        if self.tick_label_size_x is not None:
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size_x + self.font_size_increase)
        elif self.tick_label_size is not None:
            self.ax.tick_params(axis='x', labelsize=self.tick_label_size + self.font_size_increase)
        if self.tick_label_size_y is not None:
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size_y + self.font_size_increase)
        elif self.tick_label_size is not None:
            self.ax.tick_params(axis='y', labelsize=self.tick_label_size + self.font_size_increase)

        # Float format
        decimals_x = self.tick_label_decimals if isinstance(self.tick_label_decimals_x, type(None)) \
            else self.tick_label_decimals_x
        decimals_y = self.tick_label_decimals if isinstance(self.tick_label_decimals_y, type(None)) \
            else self.tick_label_decimals_y
        float_format_x = '%.' + str(decimals_x) + 'f'
        float_format_y = '%.' + str(decimals_y) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format_x))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format_y))

        # Tick-label pad
        if self.tick_label_pad is not None:
            self.ax.tick_params(axis='both', pad=self.tick_label_pad)

        # Date tick labels
        if self.tick_labels_dates_x:
            fmtd = pd.date_range(start=self.x[0], end=self.x[-1], periods=self.tick_number_x)
            fmtd = [dt.datetime.strftime(d, self.date_format) for d in fmtd]
            self.ax.set_xticklabels(fmtd)

        # Rotation
        if self.tick_rotation_x is not None:
            self.ax.tick_params(axis='x', rotation=self.tick_rotation_x)
            for tick in self.ax.xaxis.get_majorticklabels():
                tick.set_horizontalalignment("right")
        if self.tick_rotation_y is not None:
            self.ax.tick_params(axis='y', rotation=self.tick_rotation_y)
            for tick in self.ax.yaxis.get_majorticklabels():
                tick.set_horizontalalignment("left")

