# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Guides
------
"""


import numpy as np
from matplotlib.ticker import FormatStrFormatter

from mpl_plotter.utils import span


class guides:

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
            cbar.ax.yaxis.set_tick_params(pad=self.cb_tick_label_pad, labelsize=self.cb_tick_label_size)

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
                    cbar.ax.title.set_position((self.cb_title_top_x, self.cb_title_top_y))
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

    def method_grid(self):
        if self.grid:
            self.plt.grid(linestyle=self.grid_lines, color=self.grid_color)
        else:
            self.ax.grid(self.grid)
        if not self.show_axes:
            self.plt.axis('off')

    def method_legend(self):
        if self.legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=self.legend_weight,
                                                      style=self.legend_style,
                                                      size=self.legend_size+self.font_size_increase)
            self.legend = self.fig.legend(loc=self.legend_loc, prop=legend_font,
                                          handleheight=self.legend_handleheight, ncol=self.legend_columns)

    def method_tick_locs(self):
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

    def method_tick_labels(self):
        
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
