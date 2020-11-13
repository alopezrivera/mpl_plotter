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
from pylab import *

from numpy import sin, cos
from skimage import measure

from mock_data import MockData
from colormaps import ColorMaps


class MatPlotLibPublicationPlotter:
    mpl.use('Qt5Agg')

    def __init__(self,
                 fig=None,
                 ax=None,
                 shape_and_position=None,
                 font='serif',
                 light=None, dark=None,
                 usetex=False):

        rc('text', usetex=usetex)

        self.fig = fig
        self.ax = ax
        self.axes3d = ax
        self.shape_and_position = shape_and_position

        self.font = font
        self.light = light
        self.dark = dark

        # Style
        if light is None and dark is None:
            self.color = 'black'
            self.color2 = (193/256, 193/256, 193/256)
            self.style = None

        if self.light:
            self.color = 'black'
            self.color2 = (193/256, 193/256, 193/256)
            self.style = 'classic'
        elif self.dark:
            self.color = 'white'
            self.color2 = (89/256, 89/256, 89/256)
            self.style = 'dark_background'

    def setup2d(self, figsize=None):

        # Style
        if self.style is not None:
            plt.style.use(self.style)

        if isinstance(self.fig, type(None)):
            self.fig = plt.figure(figsize=figsize)

        return self.fig

    def setup3d(self, figsize=None):

        if self.style is not None:
            plt.style.use(self.style)

        if isinstance(self.fig, type(None)):
            self.fig = plt.figure(figsize=figsize)

        return self.fig

    def custom_subplots(self, widths, heights, ncols, nrows, figsize=None):

        if self.style is not None:
            plt.style.use(self.style)

        self.fig = plt.figure(figsize=figsize)

        gs_kw = dict(width_ratios=widths, height_ratios=heights)

        axes = self.fig.subplots(ncols=ncols, nrows=nrows, gridspec_kw=gs_kw)

        aux = []

        for r, row in enumerate(axes):
            if isinstance(row, list):
                for c, ax in enumerate(row):
                    aux.append(ax)
            else:
                aux.append(row)
        axes = aux

        return self.fig, axes

    def plot2d(self,
               x=None, y=None, color=None, c=None,
               x_bounds=None, y_bounds=None, xresize_pad=5, yresize_pad=5,
               line=False, linewidth=3,
               scatter=False, pointsize=5, marker='o',
               legend=False, legendloc='upper right', legend_size=13, legend_weight='normal', legend_style='normal',
               grid=False, gridcolor='black', gridlines='-',
               cmap='RdBu_r',
               color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
               cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
               cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False, cb_y_title=False,
               cb_vmin=None, cb_vmax=None,
               label=None, prune=None, resize_axes=True, custom_subplots=False, aspect=1,
               plot_title='Spirograph', title_bold=False, title_size=12, title_y=1.025,
               x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None,
               x_tick_number=10, x_ticklabels=None, y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None,
               y_tick_number=None, y_ticklabels=None, tick_color=None, tick_label_pad=5, tick_ndecimals=1,
               xtick_rotation=None, ytick_rotation=None,
               tick_label_size=None, x_ticklabel_size=None, y_ticklabel_size=None,
               more_subplots_left=False,
               filename=None, dpi=None,
               cb_top_title_pad=None,
               cb_top_title_x=0,
               custom_x_ticklabels=None, custom_y_ticklabels=None):

        if isinstance(self.fig, type(None)):
            self.setup2d()

        if isinstance(self.ax, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)):
            x, y = MockData().spirograph()

        # Plot all plots
        if line is False and scatter is False:
            line = True
        if line is True:
            graph_for_color_bar = self.ax.plot(x, y, label=label, linewidth=linewidth, color=color)
        if scatter is True:
            graph_for_color_bar = self.ax.scatter(x, y, label=label, linewidth=linewidth, s=pointsize, marker=marker,
                                                  color=color, c=c, cmap=cmap, alpha=1)

        # Colorbar
        if color_bar is True:
            vmin = float(c.min())
            vmax = float(c.max())
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight, cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Legend
        if legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=legend_weight,
                                                      style=legend_style,
                                                      size=legend_size)
            self.ax.legend(loc=legendloc, prop=legend_font)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False
        if resize_axes is True:
            self.resize_axes2d(x=x, y=y, x_bounds=x_bounds, y_bounds=y_bounds,
                               xresize_pad=xresize_pad, yresize_pad=yresize_pad, aspect=aspect)

        # Makeup
        self.makeup2d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size,
                      tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation,
                      grid=grid, prune=prune, tick_ndecimals=tick_ndecimals,
                      gridcolor=gridcolor, gridlines=gridlines,
                      x_ticklabels=x_ticklabels, y_ticklabels=y_ticklabels, x_ticklabel_size=x_ticklabel_size,
                      y_ticklabel_size=y_ticklabel_size,
                      custom_x_ticklabels=custom_x_ticklabels, custom_y_ticklabels=custom_y_ticklabels)

        # Save
        if filename:
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            self.fig.tight_layout()
            plt.show()
        else:
            print('Ready for next subplot')

        return self.ax

    def heatmap(self,
                x=None, y=None, z=None, array=None,
                x_bounds=None, y_bounds=None, xresize_pad=5, yresize_pad=5,
                resize_axes=True, custom_subplots=False, aspect=1,
                norm=None, normvariant='SymLog', grid=False, gridcolor='black', gridlines='-', prune=None,
                cmap='RdBu_r',
                color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False, cb_y_title=False,
                cb_vmin=None, cb_vmax=None,
                plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1.025,
                x_label=None, xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None,
                x_tick_number=10, x_ticklabels=None, y_label=None, yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None,
                y_tick_number=10, y_ticklabels=None, tick_color=None, tick_label_size=None, tick_label_pad=5, tick_ndecimals=1,
                xtick_rotation=None, ytick_rotation=None, axes_to_plot_pad=0,
                x_ticklabel_size=None, y_ticklabel_size=None,
                more_subplots_left=False,
                filename=None, dpi=None,
                cb_top_title_pad=None,
                cb_top_title_x=0,
                custom_x_ticklabels=None, custom_y_ticklabels=None):

        if isinstance(self.fig, type(None)):
            self.setup2d()

        if isinstance(self.ax, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position)

        # Normalization
        if norm is not None:
            norm = self.normalize(array=array, norm=norm, variant=normvariant)

        # Plot
        if not isinstance(x, type(None)) and not isinstance(y, type(None)) and not isinstance(z, type(None)):
            graph = self.ax.pcolormesh(x, y, z, cmap=cmap)
        elif not isinstance(array, type(None)):
            graph = self.ax.pcolormesh(array, cmap=cmap, norm=norm)
        else:
            # Mock plot
            array = MockData().waterdropdf()
            graph = self.ax.pcolormesh(array, cmap=cmap, norm=norm)

        # Defining xmax and xmin to allow for dataframes to be plotted
        if not isinstance(array, type(None)):
            xmin = 0
            ymin = 0
            xmax = array.shape[0]
            ymax = array.shape[1]
            if resize_axes is True and isinstance(x_bounds, type(None)):
                x_bounds = [xmin, xmax]
            if resize_axes is True and isinstance(y_bounds, type(None)):
                y_bounds = [ymin, ymax]
            z = array
        else:
            xmin = x.min()
            ymin = y.min()
            xmax = x.max()
            ymax = y.max()

        # Color_bar
        if color_bar is True:
            graph_for_color_bar = graph
        else:
            graph_for_color_bar = None

        vmin = z.min()
        vmax = z.max()

        if isinstance(cb_vmin, type(None)):
            cb_vmin = vmin
        if isinstance(cb_vmax, type(None)):
            cb_vmax = vmax
        if color_bar is True:
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad,
                           cb_title_weight=cb_title_weight, cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            self.resize_axes2d(x=x, y=y, x_bounds=x_bounds, y_bounds=y_bounds,
                               xresize_pad=xresize_pad, yresize_pad=yresize_pad, aspect=aspect)

        # Makeup
        self.makeup2d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size,
                      tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation,
                      grid=grid, prune=prune, tick_ndecimals=tick_ndecimals,
                      gridcolor=gridcolor, gridlines=gridlines,
                      x_ticklabels=x_ticklabels,
                      y_ticklabels=y_ticklabels,
                      x_ticklabel_size=x_ticklabel_size, y_ticklabel_size=y_ticklabel_size,
                      custom_x_ticklabels=custom_x_ticklabels, custom_y_ticklabels=custom_y_ticklabels)

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.ax

    def vectors2d(self,
                  x=None, y=None, u=None, v=None, rule=None, customrule=None,
                  x_bounds=None, y_bounds=None, xresize_pad=5, yresize_pad=5,
                  line=False, width_vector=0, length_min=2, length_threshold=0.1,
                  scatter=False, pointsize=5, marker='o',
                  legend=False, legendloc='upper right', legend_size=13, legend_weight='normal', legend_style='normal',
                  graph_to_size_box_around=0, grid=False, gridcolor='black', gridlines='-',
                  cmap='RdBu_r',
                  color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                  cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                  cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                  cb_y_title=False,
                  cb_vmin=None, cb_vmax=None,
                  label=None, prune=None, resize_axes=True, custom_subplots=False, aspect=1,
                  plot_title='Spirograph', title_bold=False, title_size=12, title_y=1.025,
                  x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None,
                  x_tick_number=10, x_ticklabels=None, y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None,
                  y_tick_number=None, y_ticklabels=None, tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                  xtick_rotation=None, ytick_rotation=None,
                  tick_label_size=None, x_ticklabel_size=None, y_ticklabel_size=None,
                  more_subplots_left=False,
                  filename=None, dpi=None,
                  cb_top_title_pad=None,
                  cb_top_title_x=0,
                  custom_x_ticklabels=None, custom_y_ticklabels=None):

        if isinstance(self.fig, type(None)):
            self.setup2d()

        if isinstance(self.ax, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)):
            x, y = MockData().spirograph()

        # Rule
        if isinstance(customrule, type(None)):
            if isinstance(rule, type(None)):
                rule = lambda u, v: (u ** 2 + v ** 2)
            rule = rule(u=u, v=v)
        else:
            rule = customrule

        # Color determined by rule function
        c = rule
        # Flatten and normalize
        c = (c.ravel() - c.min()) / c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(cmap)
        c = cmap(c)

        # Plot
        graph_for_color_bar = self.ax.quiver(x, y, u, v,
                                             color=c, cmap=cmap,
                                             width=width_vector,
                                             minshaft=length_min,
                                             minlength=length_threshold,
                                             )

        # Colorbar
        if color_bar is True:
            vmin = float(rule.min())
            vmax = float(rule.max())
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight, cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin if not isinstance(cb_vmin, type(None)) else vmin,
                           cb_vmax=cb_vmax if not isinstance(cb_vmax, type(None)) else vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Legend
        if legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=legend_weight,
                                                      style=legend_style,
                                                      size=legend_size)
            self.ax.legend(loc=legendloc, prop=legend_font)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False
        if resize_axes is True:
            self.resize_axes2d(x=x, y=y, x_bounds=x_bounds, y_bounds=y_bounds,
                               xresize_pad=xresize_pad, yresize_pad=yresize_pad, aspect=aspect)

        # Makeup
        self.makeup2d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size,
                      tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation,
                      grid=grid, prune=prune, tick_ndecimals=tick_ndecimals,
                      gridcolor=gridcolor, gridlines=gridlines,
                      x_ticklabels=x_ticklabels, y_ticklabels=y_ticklabels, x_ticklabel_size=x_ticklabel_size,
                      y_ticklabel_size=y_ticklabel_size,
                      custom_x_ticklabels=custom_x_ticklabels, custom_y_ticklabels=custom_y_ticklabels)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.ax

    def streamlines2d(self,
                      x=None, y=None, u=None, v=None,
                      color=None, rule_width=None,
                      x_bounds=None, y_bounds=None, xresize_pad=5, yresize_pad=5,
                      line=False, linewidth=1, density=1,
                      scatter=False, pointsize=5, marker='o',
                      legend=False, legendloc='upper right', legend_size=13, legend_weight='normal', legend_style='normal',
                      graph_to_size_box_around=0, grid=False, gridcolor='black', gridlines='-',
                      cmap='RdBu_r',
                      color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                      cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                      cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                      cb_y_title=False,
                      cb_vmin=None, cb_vmax=None,
                      label=None, prune=None, resize_axes=True, custom_subplots=False, aspect=1,
                      plot_title='Spirograph', title_bold=False, title_size=12, title_y=1.025,
                      x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None,
                      x_tick_number=10, x_ticklabels=None, y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None,
                      y_tick_number=None, y_ticklabels=None, tick_color=None, tick_label_pad=5, tick_ndecimals=1,
                      xtick_rotation=None, ytick_rotation=None,
                      tick_label_size=None, x_ticklabel_size=None, y_ticklabel_size=None,
                      more_subplots_left=False,
                      filename=None, dpi=None,
                      cb_top_title_pad=None,
                      cb_top_title_x=0,
                      custom_x_ticklabels=None, custom_y_ticklabels=None):

        if isinstance(self.fig, type(None)):
            self.setup2d()

        if isinstance(self.ax, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.ax = self.fig.add_subplot(self.shape_and_position, adjustable='box')

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)):
            x, y = MockData().spirograph()

        # Color
        # if isinstance(color, type(None)):
        #     color = u

        # Line width
        if isinstance(rule_width, type(None)):
            rule_width = lambda u: 5*(u/u.max())**2
            # linewidth = rule_width(u)

        graph_for_color_bar = self.ax.streamplot(x, y, u, v,
                                                 color=color,
                                                 cmap=cmap,
                                                 linewidth=linewidth,
                                                 density=density,
                                                 ).lines

        # Colorbar
        if color_bar is True:
            vmin = float(color.min())
            vmax = float(color.max())
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Legend
        if legend is True:
            legend_font = font_manager.FontProperties(family=self.font,
                                                      weight=legend_weight,
                                                      style=legend_style,
                                                      size=legend_size)
            self.ax.legend(loc=legendloc, prop=legend_font)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False
        if resize_axes is True:
            self.resize_axes2d(x=x, y=y, x_bounds=x_bounds, y_bounds=y_bounds,
                               xresize_pad=xresize_pad, yresize_pad=yresize_pad, aspect=aspect)

        # Makeup
        self.makeup2d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size,
                      tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation,
                      grid=grid, prune=prune, tick_ndecimals=tick_ndecimals,
                      gridcolor=gridcolor, gridlines=gridlines,
                      x_ticklabels=x_ticklabels, y_ticklabels=y_ticklabels, x_ticklabel_size=x_ticklabel_size,
                      y_ticklabel_size=y_ticklabel_size,
                      custom_x_ticklabels=custom_x_ticklabels, custom_y_ticklabels=custom_y_ticklabels)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.ax


    def line3d(self,
               x=None, x_scale=1, x_pad=0,
               y=None, y_scale=1, y_pad=0,
               z=None, z_scale=1, z_pad=0,
               line_color='darkred', alpha=1, linewidth=5,
               box_to_plot_pad=10,
               grid=False, pane_fill=False, prune=None,
               plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
               x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5,
               xlabel_rotation=None, x_tick_number=10,
               y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5,
               ylabel_rotation=None, y_tick_number=10,
               z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5,
               zlabel_rotation=None, z_tick_number=10,
               tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
               xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
               custom_subplots=False, resize_axes=True, more_subplots_left=False,
               filename=None, dpi=None,
               cb_top_title_pad=None,
               cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale/max_scale
        y_scale = y_scale/max_scale
        z_scale = z_scale/max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            x, y = MockData().sinewave()
            z = np.array([5])

        # Plot
        graph = self.axes3d.plot3D(x, y, z, alpha=alpha, linewidth=linewidth, color=line_color)

        z_pad = z_pad if z_pad > (abs(z.max())+abs(z.min()))/16 else (abs(z.max())+abs(z.min()))/16

        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size, xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size, yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size, zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      prune=prune, tick_ndecimals=tick_ndecimals)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def scatter3d(self,
                  x=None, x_scale=1, x_pad=0,
                  y=None, y_scale=1, y_pad=0,
                  z=None, z_scale=1, z_pad=0,
                  pointsize=60,
                  edge_color='b', edges_to_RGBA=True, rstride=1, cstride=1, alpha=1, linewidth=0,
                  box_to_plot_pad=10,
                  grid=False, pane_fill=False, prune=None, lighting=False, antialiased=False, shade=False,
                  norm=None, cmap='RdBu_r', c=None,
                  color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                  cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                  cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                  cb_y_title=False,
                  cb_vmin=None, cb_vmax=None,
                  plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                  x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5,
                  xlabel_rotation=None, x_tick_number=10,
                  y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5,
                  ylabel_rotation=None, y_tick_number=10,
                  z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5,
                  zlabel_rotation=None, z_tick_number=10,
                  tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                  xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                  custom_subplots=False, resize_axes=True, more_subplots_left=False,
                  filename=None, dpi=None,
                  cb_top_title_pad=None,
                  cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale/max_scale
        y_scale = y_scale/max_scale
        z_scale = z_scale/max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            x, y, z = MockData().waterdrop3d()

        # Normalization
        if norm is not None:
            norm = self.normalize(array=z, norm=norm, variant='Power')

        # Plot
        graph = self.axes3d.scatter(x, y, z, cmap=cmap,
                                    edgecolors=edge_color, alpha=alpha,
                                    norm=norm, marker='s', c=c, linewidth=linewidth, s=pointsize)

        # Edges to RGBA
        if edges_to_RGBA is True:
            graph.set_edgecolors(graph.to_rgba(graph._A))

        # Color bar
        vmin = float(z.min())
        vmax = float(z.max())

        if color_bar is True:
            graph_for_color_bar = graph
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)
        # Resize axes
        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size, xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size, yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size, zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      prune=prune, tick_ndecimals=tick_ndecimals)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def surface3d(self,
                  x=None, x_scale=1, x_pad=0,
                  y=None, y_scale=1, y_pad=0,
                  z=None, z_scale=1, z_pad=0,
                  edge_color='b', edges_to_RGBA=True, rstride=1, cstride=1, alpha=1, linewidth=0,
                  box_to_plot_pad=10,
                  grid=False, pane_fill=False, prune=None, lighting=True, antialiased=True, shade=True,
                  norm=None, cmap='RdBu_r',
                  color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                  cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                  cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                  cb_y_title=False,
                  cb_vmin=None, cb_vmax=None,
                  plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                  x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5,
                  xlabel_rotation=None, x_tick_number=10,
                  y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5,
                  ylabel_rotation=None, y_tick_number=10,
                  z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5,
                  zlabel_rotation=None, z_tick_number=10,
                  tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                  xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                  custom_subplots=False, resize_axes=True, more_subplots_left=False,
                  filename=None, dpi=None,
                  cb_top_title_pad=None,
                  cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale/max_scale
        y_scale = y_scale/max_scale
        z_scale = z_scale/max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            x, y, z = MockData().waterdrop3d()

        # Normalization
        if norm is not None:
            norm = self.normalize(array=z, norm=norm, variant='Power')

        # Plot
        graph = self.axes3d.plot_surface(x, y, z, cmap=cmap,
                                         edgecolors=edge_color, alpha=alpha,
                                         rstride=rstride, cstride=cstride, linewidth=linewidth,
                                         norm=norm, facecolors=self.lighting(z, cmap) if lighting is True else None,
                                         antialiased=antialiased, shade=shade)

        # Edges to RGBA
        if edges_to_RGBA is True:
            graph.set_edgecolors(graph.to_rgba(graph._A))

        # Color bar
        vmin = float(z.min())
        vmax = float(z.max())

        if color_bar is True:
            graph_for_color_bar = graph
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)
        # Resize axes
        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size, xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size, yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size, zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      prune=prune, tick_ndecimals=tick_ndecimals)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def tricontour(self,
                   x=None, x_scale=1, x_pad=0,
                   y=None, y_scale=1, y_pad=0,
                   z=None, z_scale=1, z_pad=0,
                   levels=5, alpha=1,
                   box_to_plot_pad=12,
                   grid=False, pane_fill=False, prune=None,
                   norm=None, cmap='RdBu_r',
                   color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                   cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                   cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                   cb_y_title=False,
                   cb_vmin=None, cb_vmax=None,
                   plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                   x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                   y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                   z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                   tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                   xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                   custom_subplots=False, resize_axes=True, more_subplots_left=False,
                   filename=None, dpi=None,
                   cb_top_title_pad=None,
                   cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale / max_scale
        y_scale = y_scale / max_scale
        z_scale = z_scale / max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            x, y, z = MockData().random3d()

        # Normalization
        if norm is not None:
            norm = self.normalize(array=z, norm=norm, variant='Power')

        # Plot
        cf = self.axes3d.tricontourf(x, y, z, levels=levels, cmap=cmap, alpha=alpha, norm=norm)

        for c in cf.collections:
            c.set_edgecolor('None')

        # Color bar

        vmin = float(z.min())
        vmax = float(z.max())

        if color_bar is True:
            graph_for_color_bar = cf
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        z_pad = z_pad if z_pad > (abs(z.max())+abs(z.min()))/4 else (abs(z.max())+abs(z.min()))/4

        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill, prune=prune,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size, xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size, yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size, zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      tick_ndecimals=tick_ndecimals)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def projections(self,
                    x=None, x_center=None, x_scale=1, x_pad=0,
                    y=None, y_center=None, y_scale=1, y_pad=0,
                    z=None, z_center=None, z_scale=1, z_pad=0, alpha=1,
                    switch=True,
                    box_to_plot_pad=12,
                    grid=False, pane_fill=False, prune=None,
                    norm=None, cmap='RdBu_r',
                    color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                    cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                    cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                    cb_y_title=False,
                    cb_vmin=None, cb_vmax=None,
                    plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                    x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                    y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                    z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                    tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                    xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                    custom_subplots=False, resize_axes=True, more_subplots_left=False,
                    filename=None, dpi=None,
                    cb_top_title_pad=None,
                    cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale / max_scale
        y_scale = y_scale / max_scale
        z_scale = z_scale / max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            x, y, z = MockData().waterdrop3d()

        # Normalization
        if norm is not None:
            norm = self.normalize(array=z, norm=norm, variant='Power')

        # Resize axes
        z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 8 else (abs(z.max()) + abs(z.min())) / 8

        self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                           x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Plot
        x_plane = self.axes3d.contourf(x, y, z, zdir='x', offset=self.axes3d.get_xlim()[0], cmap=cmap, alpha=alpha, norm=norm)
        y_plane = self.axes3d.contourf(x, y, z, zdir='y', offset=self.axes3d.get_ylim()[1], cmap=cmap, alpha=alpha, norm=norm)
        z_plane = self.axes3d.contourf(x, y, z, zdir='z', offset=self.axes3d.get_zlim()[0], cmap=cmap, alpha=alpha, norm=norm)

        for c in x_plane.collections:
            c.set_edgecolor('None')

        for c in y_plane.collections:
            c.set_edgecolor('None')

        for c in z_plane.collections:
            c.set_edgecolor('None')

        # Color bar

        vmin = min([float(x.min()), float(y.min()), float(z.min())])
        vmax = max([float(x.max()), float(y.max()), float(z.max())])

        if color_bar is True:
            graph_for_color_bar = y_plane
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)
        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()), z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill, prune=prune,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size,
                      zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def isosurface(self,
                   x=None, y=None, z=None, triangles=None,
                   x_center=None, x_scale=1, x_pad=0,
                   y_center=None, y_scale=1, y_pad=0,
                   z_center=None, z_scale=1, z_pad=0, alpha=1,
                   switch=True,
                   box_to_plot_pad=12,
                   grid=False, pane_fill=False, prune=None,
                   norm=None, cmap='RdBu_r',
                   color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                   cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                   cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                   cb_y_title=False,
                   cb_vmin=None, cb_vmax=None,
                   plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                   x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                   y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                   z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                   tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                   xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                   custom_subplots=False, resize_axes=True, more_subplots_left=False,
                   filename=None, dpi=None,
                   cb_top_title_pad=None,
                   cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale / max_scale
        y_scale = y_scale / max_scale
        z_scale = z_scale / max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)):
            def f(x, y, z):
                return cos(x) + cos(y) + cos(z)

            x, y, z = np.pi * np.mgrid[-2:2:31j, -2:2:31j, -2:2:31j]
            vol = f(x, y, z)
            verts, faces, _, _ = measure.marching_cubes_lewiner(vol, 0, spacing=(0.1, 0.1, 0.1))
            isosurface = self.axes3d.plot_trisurf(verts[:, 0], verts[:, 1], verts[:, 2], faces,
                                                  cmap='Spectral', lw=1)

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Normalization
        if norm is not None:
            norm = self.normalize(array=z, norm=norm, variant='Power')

        # Plot
        isosurface = self.axes3d.plot_trisurf(x, y, z, triangles=triangles.triangles, cmap=cmap, lw=1)

        # Color bar
        if color_bar is True:
            graph_for_color_bar = isosurface
            vmin = z.min()
            vmax = z.max()
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()),
                               z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill, prune=prune,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size,
                      zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      tick_ndecimals=tick_ndecimals,
                      cb_top_title_x=cb_top_title_x)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def vectors3D(self,
                  x=None, y=None, z=None, u=None, v=None, w=None, vectorlength=0.1, vectorwidth=1, rule=None,
                  x_scale=1, x_pad=0,
                  y_scale=1, y_pad=0,
                  z_scale=1, z_pad=0, alpha=1,
                  switch=True,
                  box_to_plot_pad=12,
                  grid=False, pane_fill=False, prune=None,
                  norm=None, cmap='RdBu_r',
                  color_bar=False, cb_title=None, cb_axis_labelpad=10, cb_nticks=10, shrink=0.75,
                  cb_outlinewidth=None, cb_title_rotation=None, cb_title_style='normal', cb_title_size=10,
                  cb_top_title_y=1, cb_ytitle_labelpad=10, cb_title_weight='normal', cb_top_title=False,
                  cb_y_title=False,
                  cb_vmin=None, cb_vmax=None,
                  plot_title='Drop - Wave function', title_bold=False, title_size=12, title_y=1,
                  x_label='x', xaxis_bold=False, xaxis_label_size=12, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                  y_label='y', yaxis_bold=False, yaxis_label_size=12, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                  z_label='z', zaxis_bold=False, zaxis_label_size=12, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                  tick_color=None, tick_label_size=7, tick_label_pad=5, tick_ndecimals=1,
                  xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                  custom_subplots=False, resize_axes=True, more_subplots_left=False,
                  filename=None, dpi=None,
                  cb_top_title_pad=None,
                  cb_top_title_x=0):

        if isinstance(self.fig, type(None)):
            self.setup3d()

        if isinstance(self.axes3d, type(None)):
            if isinstance(self.shape_and_position, type(None)):
                self.shape_and_position = 111
            self.axes3d = self.fig.add_subplot(self.shape_and_position, projection='3d')

        # Scaling
        max_scale = max(x_scale, y_scale, z_scale)
        x_scale = x_scale / max_scale
        y_scale = y_scale / max_scale
        z_scale = z_scale / max_scale

        # Reference:
        # https://stackoverflow.com/questions/30223161/matplotlib-mplot3d-how-to-increase-the-size-of-an-axis-stretch-in-a-3d-plo
        self.axes3d.get_proj = lambda: np.dot(Axes3D.get_proj(self.axes3d), np.diag([x_scale, y_scale, z_scale, 1]))

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)) and isinstance(u, type(None)) and isinstance(v, type(None)) and isinstance(w, type(None)):
            def f(x, y, z):
                return cos(x) + cos(y) + cos(z)

        # Distance from axes to limit of plot
        self.axes3d.dist = box_to_plot_pad

        # Normalization
        if norm is True:
            norm = colors.LogNorm(vmin=np.amin(np.array([u, v, w])), vmax=np.amax(np.array([u, v, w])))

        if isinstance(rule, type(None)):
            rule = lambda u, v, w: (u ** 2 + v ** 2 + w ** 2)

        rule = rule(u=u, v=v, w=w)

        # Color determined by rule function
        c = rule
        # Flatten and normalize
        c = (c.ravel() - c.min()) / c.ptp()
        # Repeat for each body line and two head lines
        c = np.concatenate((c, np.repeat(c, 2)))
        # Colormap
        cmap = mpl.cm.get_cmap(cmap)
        c = cmap(c)

        # Plot
        quiver = self.axes3d.quiver(x, y, z, u, v, w, length=vectorlength, linewidths=vectorwidth, pivot='tail', colors=c, cmap=cmap)

        # Color bar
        if color_bar is True:
            graph_for_color_bar = quiver
            vmin = rule.min()
            vmax = rule.max()
            self.color_bar(graph_for_color_bar=graph_for_color_bar, cb_top_title_pad=cb_top_title_pad,
                           cb_axis_labelpad=cb_axis_labelpad, cb_nticks=cb_nticks, shrink=shrink, norm=norm,
                           cb_outlinewidth=cb_outlinewidth, cb_title=cb_title, cb_title_rotation=cb_title_rotation,
                           cb_title_size=cb_title_size, cb_title_style=cb_title_style,
                           cb_ytitle_labelpad=cb_ytitle_labelpad, cb_title_weight=cb_title_weight,
                           cb_y_title=cb_y_title,
                           cb_top_title=cb_top_title, cb_top_title_y=cb_top_title_y,
                           cb_vmin=cb_vmin, cb_vmax=cb_vmax,
                           tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        # Resize axes
        if custom_subplots is True:
            resize_axes = False

        if resize_axes is True:
            z_pad = z_pad if z_pad > (abs(z.max()) + abs(z.min())) / 16 else (abs(z.max()) + abs(z.min())) / 16
            self.resize_axes3d(x_bounds=(x.min(), x.max()), y_bounds=(y.min(), y.max()),
                               z_bounds=(z.min(), z.max()),
                               x_pad=x_pad, y_pad=y_pad, z_pad=z_pad)

        # Makeup
        self.makeup3d(plot_title=plot_title, title_bold=title_bold, title_size=title_size, title_y=title_y,
                      grid=grid, pane_fill=pane_fill, prune=prune,
                      x_label=x_label, xaxis_bold=xaxis_bold, xaxis_label_size=xaxis_label_size,
                      xaxis_labelpad=xaxis_labelpad, xlabel_rotation=xlabel_rotation, x_tick_number=x_tick_number,
                      y_label=y_label, yaxis_bold=yaxis_bold, yaxis_label_size=yaxis_label_size,
                      yaxis_labelpad=yaxis_labelpad, ylabel_rotation=ylabel_rotation, y_tick_number=y_tick_number,
                      z_label=z_label, zaxis_bold=zaxis_bold, zaxis_label_size=zaxis_label_size,
                      zaxis_labelpad=zaxis_labelpad, zlabel_rotation=zlabel_rotation, z_tick_number=z_tick_number,
                      tick_color=tick_color, tick_label_size=tick_label_size, tick_label_pad=tick_label_pad,
                      xtick_rotation=xtick_rotation, ytick_rotation=ytick_rotation, ztick_rotation=ztick_rotation,
                      tick_ndecimals=tick_ndecimals,
                           cb_top_title_x=cb_top_title_x)

        self.fig.tight_layout()

        # Save
        if not isinstance(filename, type(None)):
            plt.savefig(filename, dpi=dpi)

        # More subplots
        if more_subplots_left is not True:
            plt.show()
        else:
            print('Ready for next subplot')

        return self.axes3d

    def floating_text2d(self, text, x, y, size=20, weight='normal', color='darkred'):
        # Font
        font = {'family': self.font,
                'color': color,
                'weight': weight,
                'size': size,
                }
        # Floating text
        self.ax.text(x, y, text, size=size, weight=weight, fontdict=font)

    def floating_text3d(self, text, x, y, z, size=20, weight='normal', color='darkred'):
        # Font
        font = {'family': self.font,
                'color': color,
                'weight': weight,
                'size': size,
                }
        # Floating text
        self.axes3d.text(x, y, z, text, size=size, weight=weight, fontdict=font)

    def makeup2d(self,
                 plot_title, title_bold, title_size, title_y,
                 x_label, xaxis_bold, xaxis_label_size, xaxis_labelpad, xlabel_rotation, x_tick_number, x_ticklabels,
                 y_label, yaxis_bold, yaxis_label_size, yaxis_labelpad, ylabel_rotation, y_tick_number, y_ticklabels,
                 tick_color, tick_label_size, tick_label_pad, tick_ndecimals,
                 xtick_rotation, ytick_rotation, x_ticklabel_size, y_ticklabel_size,
                 grid, prune, gridcolor, gridlines, custom_x_ticklabels, custom_y_ticklabels):

        # Background color
        self.ax.patch.set_alpha(1)

        # Title
        if not isinstance(plot_title, type(None)):
            if title_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_title(plot_title, fontname=self.font, weight=weight,
                              color=self.color, size=title_size)
            self.ax.title.set_position((0.5, title_y))

        # Axis labels
        if x_label is not None:
            if xaxis_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_xlabel(x_label, fontname=self.font, weight=weight,
                               color=self.color, size=xaxis_label_size, labelpad=xaxis_labelpad, rotation=xlabel_rotation)
        if y_label is not None:
            if yaxis_bold is True:
                weight = 'bold'
            else:
                weight = 'normal'
            self.ax.set_ylabel(y_label, fontname=self.font, weight=weight,
                               color=self.color, size=yaxis_label_size, labelpad=yaxis_labelpad, rotation=ylabel_rotation)

        # Spines
        #   Color
        spine_color = self.color
        self.ax.spines['bottom'].set_color(spine_color)
        self.ax.spines['left'].set_color(spine_color)
        #   Remove top and right spines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.tick_params(axis='both', which='both', top=False, right=False)

        # Ticks
        #   Tick-label distance
        self.ax.xaxis.set_tick_params(pad=0.1, direction='in')
        self.ax.yaxis.set_tick_params(pad=0.1, direction='in')
        #   Color
        if tick_color is not None:
            self.ax.tick_params(axis='both', color=tick_color)
        #   Label font and color
        for tick in self.ax.get_xticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.color)
        for tick in self.ax.get_yticklabels():
            tick.set_fontname(self.font)
            tick.set_color(self.color)
        #   Label size
        if not isinstance(x_ticklabel_size, type(None)):
            self.ax.tick_params(axis='x', labelsize=x_ticklabel_size)
        if not isinstance(y_ticklabel_size, type(None)):
            self.ax.tick_params(axis='y', labelsize=y_ticklabel_size)
        if not isinstance(tick_label_size, type(None)):
            self.ax.tick_params(axis='both', labelsize=tick_label_size)
        #   Number and custom position ---------------------------------------------------------------------------------
        if not isinstance(x_tick_number, type(None)):
            self.ax.set_xticks(np.linspace(x_ticklabels[0] if not isinstance(x_ticklabels, type(None)) else self.ax.get_xlim()[0],
                                           x_ticklabels[1] if not isinstance(x_ticklabels, type(None)) else self.ax.get_xlim()[1],
                                           x_tick_number))
        if not isinstance(y_tick_number, type(None)):
            self.ax.set_yticks(np.linspace(y_ticklabels[0] if not isinstance(y_ticklabels, type(None)) else self.ax.get_ylim()[0],
                                           y_ticklabels[1] if not isinstance(y_ticklabels, type(None)) else self.ax.get_ylim()[1],
                                           y_tick_number))
        #   Prune
        if not isinstance(prune, type(None)):
            self.ax.xaxis.set_major_locator(plt.MaxNLocator(prune=prune))
        if not isinstance(prune, type(None)):
            self.ax.yaxis.set_major_locator(plt.MaxNLocator(prune=prune))
        #   Float format
        float_format = '%.' + str(tick_ndecimals) + 'f'
        self.ax.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.ax.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        #   Custom tick labels
        if not isinstance(custom_x_ticklabels, type(None)):
            self.ax.set_xticklabels(np.round(np.linspace(custom_x_ticklabels[0],
                                                         custom_x_ticklabels[1],
                                                         x_tick_number),
                                             tick_ndecimals))
        if not isinstance(custom_y_ticklabels, type(None)):
            self.ax.set_yticklabels(np.round(np.linspace(custom_y_ticklabels[0],
                                                         custom_y_ticklabels[1],
                                                         y_tick_number),
                                             tick_ndecimals))
        #   Tick-label pad ---------------------------------------------------------------------------------------------
        if tick_label_pad is not None:
            self.ax.tick_params(axis='both', pad=tick_label_pad)
        #   Rotation
        if xtick_rotation is not None:
            self.ax.tick_params(axis='x', rotation=xtick_rotation)
        if ytick_rotation is not None:
            self.ax.tick_params(axis='y', rotation=ytick_rotation)

        # Grid
        if grid is not False:
            plt.grid(linestyle=gridlines, color=gridcolor)

    def makeup3d(self,
                 plot_title, title_bold, title_size, title_y,
                 grid, pane_fill, prune,
                 x_label, xaxis_bold, xaxis_label_size, xaxis_labelpad, xlabel_rotation, x_tick_number,
                 y_label, yaxis_bold, yaxis_label_size, yaxis_labelpad, ylabel_rotation, y_tick_number,
                 z_label, zaxis_bold, zaxis_label_size, zaxis_labelpad, zlabel_rotation, z_tick_number,
                 tick_color, tick_label_size, tick_label_pad, tick_ndecimals,
                 xtick_rotation, ytick_rotation, ztick_rotation):

        # Title
        if plot_title is not None:
            self.axes3d.set_title(plot_title, y=title_y, fontname=self.font, weight='bold' if title_bold else None,
                                  color=self.color, size=title_size)

        # Axis labels
        if x_label is not None:
            self.axes3d.set_xlabel(x_label, fontname=self.font, weight='bold' if xaxis_bold else None,
                                   color=self.color, size=xaxis_label_size, labelpad=xaxis_labelpad,
                                   rotation=xlabel_rotation)
        if y_label is not None:
            self.axes3d.set_ylabel(y_label, fontname=self.font, weight='bold' if yaxis_bold else None,
                                   color=self.color, size=yaxis_label_size, labelpad=yaxis_labelpad,
                                   rotation=ylabel_rotation)
        if z_label is not None:
            self.axes3d.set_zlabel(z_label, fontname=self.font, weight='bold' if zaxis_bold else None,
                                   color=self.color, size=zaxis_label_size, labelpad=zaxis_labelpad,
                                   rotation=zlabel_rotation)

        # Ticks
        #   Color
        if tick_color is not None:
            self.axes3d.tick_params(axis='both', color=tick_color)

            self.axes3d.w_xaxis.line.set_color(tick_color)
            self.axes3d.w_yaxis.line.set_color(tick_color)
            self.axes3d.w_zaxis.line.set_color(tick_color)
        #   Label size
        if tick_label_size is not None:
            self.axes3d.tick_params(axis='both', labelsize=tick_label_size)
        #   Numeral size
        for tick in self.axes3d.get_xticklabels():
            tick.set_fontname(self.font)
        for tick in self.axes3d.get_yticklabels():
            tick.set_fontname(self.font)
        for tick in self.axes3d.get_zticklabels():
            tick.set_fontname(self.font)
        #   Float format
        float_format = '%.'+str(tick_ndecimals)+'f'
        self.axes3d.xaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.axes3d.yaxis.set_major_formatter(FormatStrFormatter(float_format))
        self.axes3d.zaxis.set_major_formatter(FormatStrFormatter(float_format))

        # Tick number
        if x_tick_number is not None:
            self.axes3d.xaxis.set_major_locator(plt.MaxNLocator(x_tick_number, prune=prune))
        if y_tick_number is not None:
            self.axes3d.yaxis.set_major_locator(plt.MaxNLocator(y_tick_number, prune=prune))
        if z_tick_number is not None:
            self.axes3d.zaxis.set_major_locator(plt.MaxNLocator(z_tick_number, prune=prune))

        # Tick label pad
        if tick_label_pad is not None:
            self.axes3d.tick_params(axis='both', pad=tick_label_pad)

        # Tick rotation
        if xtick_rotation is not None:
            self.axes3d.tick_params(axis='x', rotation=xtick_rotation)
        if ytick_rotation is not None:
            self.axes3d.tick_params(axis='y', rotation=ytick_rotation)
        if ytick_rotation is not None:
            self.axes3d.tick_params(axis='z', rotation=ztick_rotation)

        # Grid
        self.axes3d.grid(grid)

        # Pane fill and pane edge color
        self.axes3d.xaxis.pane.fill = pane_fill
        self.axes3d.yaxis.pane.fill = pane_fill
        self.axes3d.zaxis.pane.fill = pane_fill
        self.axes3d.xaxis.pane.set_edgecolor(tick_color)
        self.axes3d.yaxis.pane.set_edgecolor(tick_color)

    def resize_axes2d(self, aspect, x, y, x_bounds, y_bounds, xresize_pad, yresize_pad):
        if isinstance(x_bounds, type(None)):
            x_bounds = [x.min(), x.max()]
        else:
            xresize_pad = 0
        if isinstance(y_bounds, type(None)):
            y_bounds = [y.min(), y.max()]
        else:
            yresize_pad = 0

        self.ax.set_aspect(aspect)
        self.ax.set_xbound(lower=x_bounds[0] - xresize_pad, upper=x_bounds[1] + xresize_pad)
        self.ax.set_ybound(lower=y_bounds[0] - yresize_pad, upper=y_bounds[1] + yresize_pad)

        self.ax.set_xlim(x_bounds[0] - xresize_pad, x_bounds[1] + xresize_pad)
        self.ax.set_ylim(y_bounds[0] - yresize_pad, y_bounds[1] + yresize_pad)

    def resize_axes3d(self, x_bounds=None, y_bounds=None, z_bounds=None, x_pad=0, y_pad=0, z_pad=0):
        if x_bounds is not None:
            self.axes3d.set_xlim3d(x_bounds[0]-x_pad, x_bounds[1]+x_pad)
        if y_bounds is not None:
            self.axes3d.set_ylim3d(y_bounds[0]-y_pad, y_bounds[1]+y_pad)
        if z_bounds is not None:
            self.axes3d.set_zlim3d(z_bounds[0]-z_pad, z_bounds[1]+z_pad)

    def color_bar(self, graph_for_color_bar, cb_title, cb_title_rotation, cb_ytitle_labelpad, cb_nticks,
                  shrink, norm, cb_outlinewidth, cb_title_size, cb_title_style, cb_title_weight, cb_axis_labelpad,
                  cb_y_title, cb_top_title, cb_top_title_y, cb_vmin, cb_vmax, cb_top_title_pad, tick_ndecimals,
                  cb_top_title_x):

        # Take limits from plot
        graph_for_color_bar.set_clim([cb_vmin, cb_vmax])

        # Normalization
        if norm is None:
            locator = np.linspace(cb_vmin, cb_vmax, cb_nticks, endpoint=True)
        else:
            locator = None

        # Colorbar
        cbar = self.fig.colorbar(graph_for_color_bar, spacing='proportional', ticks=locator, shrink=shrink,
                                 extend='max', norm=None, orientation='vertical',
                                 ax=self.axes3d if not isinstance(self.axes3d, type(None)) else self.ax,
                                 format='%.' + str(tick_ndecimals) + 'f')

        # Ticks
        #   Direction
        cbar.ax.tick_params(axis='y', direction='out')
        #   Tick label pad and size
        cbar.ax.yaxis.set_tick_params(pad=cb_axis_labelpad, labelsize=10)

        # Title
        if not isinstance(cb_title, type(None)) and cb_y_title is False and cb_top_title is False:
            print('Input colorbar title location with booleans: cb_y_title=True or cb_top_title=True')
        if cb_y_title is True:
            cbar.ax.set_ylabel(cb_title, rotation=cb_title_rotation, labelpad=cb_ytitle_labelpad)
            text = cbar.ax.yaxis.label
            font = matplotlib.font_manager.FontProperties(family=self.font, style=cb_title_style, size=cb_title_size,
                                                          weight=cb_title_weight)
            text.set_font_properties(font)
        if cb_top_title is True:
            cbar.ax.set_title(cb_title, rotation=cb_title_rotation, fontdict={'verticalalignment': 'baseline',
                                                                              'horizontalalignment': 'left'},
                              pad=cb_top_title_pad)
            cbar.ax.title.set_position((cb_top_title_x, cb_top_title_y))
            text = cbar.ax.title
            font = matplotlib.font_manager.FontProperties(family=self.font, style=cb_title_style, weight=cb_title_weight,
                                                          size=cb_title_size)
            text.set_font_properties(font)

        # Outline
        cbar.outline.set_edgecolor(self.color2)
        cbar.outline.set_linewidth(cb_outlinewidth)

    def normalize(self, array, norm, variant):
        if variant == 'SymLog':
            vmin = float(array.min())
            temp = 0

            # Temp raise plot to normalize
            if vmin < 0:
                array = array - vmin
                temp = vmin

            vmax = float(array.max())
            vmin = norm * vmax

            # Revert to original position
            vmax = vmax + temp
            vmin = vmin + temp

            norm = colors.SymLogNorm(base=np.e, linthresh=0.03, linscale=0.03, vmin=vmin, vmax=vmax)

            return norm

        if variant == 'MidPoint':
            vmin = float(array.min())
            vmax = float(array.max())

            range = abs(vmax)+abs(vmin)

            vcenter = vmin + range*norm

            x, y = [vmin, 0.01, vmax], [0, 0.5, 1]
            norm = np.ma.masked_array(np.interp(1, x, y))

            return norm

        if variant == 'Power':
            return colors.PowerNorm(gamma=norm)

    def lighting(self, z, cmap):
        ls = LightSource(270, 45)
        rgb = ls.shade(z, cmap=cm.get_cmap(cmap), vert_exag=0.1, blend_mode='soft')
        return rgb
