import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go

from data_input import Data3D

from colormaps import ColorMaps


class PlotLyPublicationPlotter:

    pio.renderers.default = "browser"

    def __init__(self,
                 font='Serif',
                 dark=False,
                 cmap='gnuplot2',
                 reverse_cmap_x=True,
                 reverse_cmap_y=True,
                 reverse_cmap_z=True,
                 alpha=1):

        self.font = font
        self.dark = dark

        # Style
        self.color = 'black'
        self.color2 = 'rgb(193, 193, 193)'
        self.template = 'plotly_white'

        if self.dark:
            self.color = 'white'
            self.color2 = 'rgb(89, 89, 89)'
            self.template = 'plotly_dark'

        custom = ColorMaps().mpl_cmap_to_plotly(cmap)

        self.cmap = custom

        self.cmap_x = custom
        self.cmap_y = custom
        self.cmap_z = custom

        self.reverse_cmap_x = reverse_cmap_x
        self.reverse_cmap_y = reverse_cmap_y
        self.reverse_cmap_z = reverse_cmap_z

        self.alpha = alpha

    def intersection3d(self,
                       function=None,
                       w=700, h=700, res=50, grid=True, pane_fill=None, prune=None,
                       x_slice=True, x_center=None, x_scale=1, x_lim=None,
                       y_slice=True, y_center=-3.5, y_scale=1, y_lim=None,
                       z_slice=True, z_center=None, z_scale=1, z_lim=None,
                       norm=None, cb_labelpad=10, cb_nticks=10, cb_x=None, cb_y=None,
                       cb_title=None, cb_length=0.75, cb_outlinecolor=None, cb_outlinewidth=1, cb_tickfontsize=10,
                       plot_title='Airstream', title_bold=True, title_size=20, title_pad=5, title_y=0.85,
                       x_label='x', xaxis_bold=False, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                       y_label='y', yaxis_bold=False, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                       z_label='z', zaxis_bold=False, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                       axis_label_size=20, tick_color=None, tick_label_size=12, tick_label_pad=5,
                       xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                       floating_text=None,
                       filename=None):

        # Function
        if isinstance(function, type(None)):
            self.function = lambda x, y, z: 5 - 1 / np.exp(np.sqrt(z ** 2 + x ** 2))

        # Colorbar parameters
        self.cb_outlinecolor = cb_outlinecolor if cb_outlinecolor is not None else self.color2
        self.cb_outlinewidth = cb_outlinewidth
        self.cb_length = cb_length
        self.cb_title = cb_title
        self.cb_x = cb_x
        self.cb_y = cb_y
        self.cb_xpad = cb_labelpad
        self.cb_nticks = cb_nticks
        self.cb_tickfontsize = cb_tickfontsize

        # Mock plot
        # if x is None and y is None and z is None:
        #     x, y, z = MockData().waterdrop3d()
        x = np.linspace(-5, 5, res)
        y = np.linspace(-5, 5, res)
        z = np.linspace(-5, 5, res)

        surface_shape = (res, res)

        sminx, smaxx = None, None
        sminy, smaxy = None, None
        sminz, smaxz = None, None

        # Slice string
        data = []

        # Slice in X
        if x_slice is True:
            # Check for plane location
            if x_center is None:
                x_center = 0
            x_slice, sminx, smaxx = self.horizontal_slice(plane_axis='x', ax2=y, ax3=z,
                                                          plane_axis_shape=surface_shape, plane_axis_center=x_center)

        # Slice in y
        if y_slice is True:
            # Check for plane location
            if y_center is None:
                y_center = 0
            y_slice, sminy, smaxy = self.horizontal_slice(plane_axis='y', ax2=x, ax3=z,
                                                          plane_axis_shape=surface_shape, plane_axis_center=y_center)

        # Slice in Z
        if z_slice is True:
            # Check for plane location
            if z_center is None:
                z_center = 0
            z_slice, sminz, smaxz = self.horizontal_slice(plane_axis='z', ax2=x, ax3=y,
                                                          plane_axis_shape=surface_shape, plane_axis_center=z_center)

        # Colormap values and append to plot data
        vmin = min(x for x in [sminx, sminy, sminz] if x is not None)
        vmax = max(x for x in [smaxx, smaxy, smaxz] if x is not None)

        if type(x_slice) is not bool:
            x_slice.update(cmin=vmin, cmax=vmax, showscale=True)
            data.append(x_slice)

        if type(y_slice) is not bool:
            y_slice.update(cmin=vmin, cmax=vmax, showscale=True)
            data.append(y_slice)

        if type(z_slice) is not bool:
            z_slice.update(cmin=vmin, cmax=vmax, showscale=True)
            data.append(z_slice)

        # Individual axis setup
        axis = dict(showbackground=True,
                    backgroundcolor=pane_fill,
                    showgrid=grid,
                    gridcolor=self.color2,
                    zerolinecolor=self.color2,
                    tickfont={'family': self.font,
                              'size': tick_label_size,
                              'color': tick_color},
                    titlefont={'family': self.font,
                               'size': axis_label_size},
                    )

        # Layout
        layout = go.Layout(
            width=w,
            height=h,
            scene=dict(xaxis=dict(axis, range=x_lim, tickangle=xtick_rotation, nticks=x_tick_number, title='<b>'+x_label+'</b>' if xaxis_bold is True else x_label),
                       yaxis=dict(axis, range=y_lim, tickangle=ytick_rotation, nticks=y_tick_number, title='<b>'+y_label+'</b>' if yaxis_bold is True else y_label),
                       zaxis=dict(axis, range=z_lim, tickangle=ztick_rotation, nticks=z_tick_number, title='<b>'+z_label+'</b>' if zaxis_bold is True else z_label),
                       aspectratio=dict(x=x_scale, y=y_scale, z=z_scale)
                       ),
            template=self.template
        )

        # Plot
        fig = go.Figure(data=data, layout=layout)

        # Makeup
        fig.update_layout(
            title={'text': '<b>'+plot_title+'<b>' if title_bold is True else plot_title,
                   'x': 0.5,
                   'y': title_y,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(
                family=self.font,
                size=title_size,
                color=self.color,
            )
        )

        fig.show()

        if not isinstance(filename, type(None)):
            self.save(fig=fig, filename=filename)

    def get_lim_colors(self, surfacecolor):  # color limits for a slice
        return np.min(surfacecolor), np.max(surfacecolor)

    def get_the_slice(self, x, y, z, cmap, reverse_cmap, surfacecolor, showscale=False):
        return go.Surface(x=x,
                          y=y,
                          z=z,
                          surfacecolor=surfacecolor,
                          colorscale=cmap,
                          reversescale=reverse_cmap,
                          showscale=showscale,
                          colorbar=dict(thickness=20, ticklen=4,
                                        tickfont=dict(family=self.font,
                                                      size=self.cb_tickfontsize,
                                                      color=self.color),
                                        tickcolor=self.color2, nticks=self.cb_nticks, ticks='outside',
                                        outlinecolor=self.cb_outlinecolor,
                                        outlinewidth=self.cb_outlinewidth,
                                        len=self.cb_length, lenmode='fraction',
                                        title=self.cb_title, x=self.cb_x, y=self.cb_y,
                                        xpad=self.cb_xpad),
                          opacity=self.alpha)

    def horizontal_slice(self, plane_axis, ax2, ax3, plane_axis_shape, plane_axis_center):
        ax2, ax3 = np.meshgrid(ax2, ax3)
        ax1 = plane_axis_center * np.ones(plane_axis_shape)

        if plane_axis == 'x':
            x = ax1
            y = ax2
            z = ax3
            cmap = self.cmap_x
            reverse_cmap = self.reverse_cmap_x

        if plane_axis == 'y':
            x = ax2
            y = ax1
            z = ax3
            cmap = self.cmap_y
            reverse_cmap = self.reverse_cmap_y

        if plane_axis == 'z':
            x = ax2
            y = ax3
            z = ax1
            cmap = self.cmap_z
            reverse_cmap = self.reverse_cmap_z

        surfcolor = self.function(x, y, z)
        sminz, smaxz = self.get_lim_colors(surfcolor)
        slice = self.get_the_slice(x, y, z, cmap, reverse_cmap, surfcolor)

        return slice, sminz, smaxz

    def oblique_slice(self, plane_axis, ax2, ax3, alpha=np.pi/4, plane_axis_center=0):
        ax2, ax3 = np.meshgrid(ax2, ax3)
        ax1 = -ax2 * np.tan(alpha) + plane_axis_center

        if plane_axis == 'x':
            x = ax1
            y = ax2
            z = ax3
            cmap = self.cmap_x
            reverse_cmap = self.reverse_cmap_x

        if plane_axis == 'y':
            x = ax2
            y = ax1
            z = ax3
            cmap = self.cmap_y
            reverse_cmap = self.reverse_cmap_y

        if plane_axis == 'z':
            x = ax2
            y = ax3
            z = ax1
            cmap = self.cmap_z
            reverse_cmap = self.reverse_cmap_z

        surfcolor = self.function(x, y, z)
        sminz, smaxz = self.get_lim_colors(surfcolor)
        slice = self.get_the_slice(x, y, z, cmap, reverse_cmap, surfcolor)

        return slice, sminz, smaxz

    def volume(self,
               x=None, y=None, z=None, vol=None,
               w=700, h=700, res=50, grid=True, pane_fill=None, prune=None,
               x_slice=True, x_center=None, x_scale=1, x_lim=None,
               y_slice=True, y_center=-3.5, y_scale=1, y_lim=None,
               z_slice=True, z_center=None, z_scale=1, z_lim=None,
               norm=None, cb_labelpad=10, cb_nticks=10, cb_x=None, cb_y=None,
               cb_title=None, cb_length=0.75, cb_outlinecolor=None, cb_outlinewidth=1, cb_tickfontsize=10,
               plot_title='Airstream', title_bold=True, title_size=20, title_pad=5, title_y=0.85,
               x_label='x', xaxis_bold=False, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
               y_label='y', yaxis_bold=False, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
               z_label='z', zaxis_bold=False, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
               axis_label_size=20, tick_color=None, tick_label_size=12, tick_label_pad=5,
               xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
               floating_text=None,
               filename=None):

        # Colorbar parameters
        self.cb_outlinecolor = cb_outlinecolor if cb_outlinecolor is not None else self.color2
        self.cb_outlinewidth = cb_outlinewidth
        self.cb_length = cb_length
        self.cb_title = cb_title
        self.cb_x = cb_x
        self.cb_y = cb_y
        self.cb_xpad = cb_labelpad
        self.cb_nticks = cb_nticks
        self.cb_tickfontsize = cb_tickfontsize

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)) and isinstance(vol, type(None)):
            np.random.seed(0)
            def f(x, y, z):
                return x+y+z
            x, y, z, vol = Data3D().volumetric(f, u0=0, un=1, v0=0, vn=1, w0=0, wn=1, n=100)

        # Individual axis setup
        axis = dict(showbackground=True,
                    backgroundcolor=pane_fill,
                    showgrid=grid,
                    gridcolor=self.color2,
                    zerolinecolor=self.color2,
                    tickfont={'family': self.font,
                              'size': tick_label_size,
                              'color': tick_color},
                    titlefont={'family': self.font,
                               'size': axis_label_size},
                    )

        # Layout
        layout = go.Layout(
            width=w,
            height=h,
            scene=dict(xaxis=dict(axis, range=x_lim, tickangle=xtick_rotation, nticks=x_tick_number, title='<b>'+x_label+'</b>' if xaxis_bold is True else x_label),
                       yaxis=dict(axis, range=y_lim, tickangle=ytick_rotation, nticks=y_tick_number, title='<b>'+y_label+'</b>' if yaxis_bold is True else y_label),
                       zaxis=dict(axis, range=z_lim, tickangle=ztick_rotation, nticks=z_tick_number, title='<b>'+z_label+'</b>' if zaxis_bold is True else z_label),
                       aspectratio=dict(x=x_scale, y=y_scale, z=z_scale)
                       ),
            template=self.template
        )

        # Plot
        fig = go.Figure(data=go.Volume(x=x, y=y, z=z,
                                       value=vol,
                                       isomin=0.2,
                                       isomax=0.7,
                                       opacity=0.1,
                                       surface_count=25,
                                       colorbar=dict(len=self.cb_length,
                                                     x=self.cb_x,
                                                     xpad=self.cb_xpad,
                                                     y=self.cb_y,
                                                     outlinecolor=self.cb_outlinecolor,
                                                     outlinewidth=self.cb_outlinewidth,
                                                     tick0=0,
                                                     dtick=0.5,
                                                     ticklen=5,
                                                     tickwidth=1,
                                                     tickfont=dict(size=self.cb_tickfontsize,
                                                                   color=self.color,
                                                                   family=self.font),
                                                     title=self.cb_title)
                                       ),
                        layout=layout)

        # Makeup
        fig.update_layout(
            title={'text': '<b>'+plot_title+'<b>' if title_bold is True else plot_title,
                   'x': 0.5,
                   'y': title_y,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(
                family=self.font,
                size=title_size,
                color=self.color,
            )
        )

        fig.show()

        if not isinstance(filename, type(None)):
            self.save(fig=fig, filename=filename)

    def cones(self,
              x=None, y=None, z=None, u=None, v=None, w=None, conesize=40,
              width=700, height=700, res=50, grid=True, pane_fill=None, prune=None,
              x_slice=True, x_center=None, x_scale=1, x_lim=None,
              y_slice=True, y_center=-3.5, y_scale=1, y_lim=None,
              z_slice=True, z_center=None, z_scale=1, z_lim=None,
              norm=None, cb_labelpad=10, cb_nticks=10, cb_x=None, cb_y=None,
              cb_title=None, cb_length=0.75, cb_outlinecolor=None, cb_outlinewidth=1, cb_tickfontsize=10,
              plot_title='Airstream', title_bold=True, title_size=20, title_pad=5, title_y=0.85,
              x_label='x', xaxis_bold=False, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
              y_label='y', yaxis_bold=False, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
              z_label='z', zaxis_bold=False, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
              axis_label_size=20, tick_color=None, tick_label_size=12, tick_label_pad=5,
              xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
              floating_text=None,
              filename=None):

        # Colorbar parameters
        self.cb_outlinecolor = cb_outlinecolor if cb_outlinecolor is not None else self.color2
        self.cb_outlinewidth = cb_outlinewidth
        self.cb_length = cb_length
        self.cb_title = cb_title
        self.cb_x = cb_x
        self.cb_y = cb_y
        self.cb_xpad = cb_labelpad
        self.cb_nticks = cb_nticks
        self.cb_tickfontsize = cb_tickfontsize

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)) \
                and isinstance(u, type(None)) and isinstance(v, type(None)) and isinstance(w, type(None)):
            df = pd.read_csv(
                r"C:\Users\xXY4n\AE BSc\AE Year 2\Aerodynamics project\Data Analysis\data\velocity_planes_of_interest\x=-10\x=-10_projected\-10_-8_7.csv",
                index_col=0)
            df.columns = list('--xyzuvw')
            x, y, z, u, v, w = df['x'], df['y'], df['z'], df['u'], df['v'], df['w']
            x_scale = (abs(x.max())+abs(x.min()))/max(abs(x.max())+abs(x.min()), abs(y.max())+abs(y.min()), abs(z.max())+abs(z.min()))
            y_scale = (abs(y.max())+abs(y.min()))/max(abs(x.max())+abs(x.min()), abs(y.max())+abs(y.min()), abs(z.max())+abs(z.min()))
            z_scale = (abs(z.max())+abs(z.min()))/max(abs(x.max())+abs(x.min()), abs(y.max())+abs(y.min()), abs(z.max())+abs(z.min()))

        # Individual axis setup
        axis = dict(showbackground=True,
                    backgroundcolor=pane_fill,
                    showgrid=grid,
                    gridcolor=self.color2,
                    zerolinecolor=self.color2,
                    tickfont={'family': self.font,
                              'size': tick_label_size,
                              'color': tick_color},
                    titlefont={'family': self.font,
                               'size': axis_label_size},
                    )

        # Layout
        layout = go.Layout(
            width=width,
            height=height,
            scene=dict(xaxis=dict(axis, range=x_lim, tickangle=xtick_rotation, nticks=x_tick_number, title='<b>'+x_label+'</b>' if xaxis_bold is True else x_label),
                       yaxis=dict(axis, range=y_lim, tickangle=ytick_rotation, nticks=y_tick_number, title='<b>'+y_label+'</b>' if yaxis_bold is True else y_label),
                       zaxis=dict(axis, range=z_lim, tickangle=ztick_rotation, nticks=z_tick_number, title='<b>'+z_label+'</b>' if zaxis_bold is True else z_label),
                       aspectratio=dict(x=x_scale, y=y_scale, z=z_scale)
                       ),
            template=self.template
        )

        # Plot
        fig = go.Figure(data=go.Cone(x=x,
                                     y=y,
                                     z=z,
                                     u=u,
                                     v=v,
                                     w=w,
                                     colorscale=self.cmap,
                                     sizemode='absolute',
                                     sizeref=conesize,
                                     colorbar=dict(len=self.cb_length,
                                                   x=self.cb_x,
                                                   xpad=self.cb_xpad,
                                                   y=self.cb_y,
                                                   outlinecolor=self.cb_outlinecolor,
                                                   outlinewidth=self.cb_outlinewidth,
                                                   tick0=0,
                                                   dtick=0.5,
                                                   ticklen=5,
                                                   tickwidth=1,
                                                   tickfont=dict(size=self.cb_tickfontsize,
                                                                 color=self.color,
                                                                 family=self.font),
                                                   title=self.cb_title)
                                     ),
                        layout=layout)

        # Makeup
        fig.update_layout(
            title={'text': '<b>'+plot_title+'<b>' if title_bold is True else plot_title,
                   'x': 0.5,
                   'y': title_y,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(
                family=self.font,
                size=title_size,
                color=self.color,
            )
        )

        fig.show()

        if not isinstance(filename, type(None)):
            self.save(fig=fig, filename=filename)

    def scatter3D(self,
                  fig=None,
                  x=None, y=None, z=None, c=None,
                  pointsize=5, symbol='square', opacity=0.8, showlegend=False,
                  w=700, h=700, res=50, grid=True, pane_fill=None, prune=None,
                  x_slice=True, x_center=None, x_scale=40/30, x_lim=None,
                  y_slice=True, y_center=-3.5, y_scale=1, y_lim=None,
                  z_slice=True, z_center=None, z_scale=1, z_lim=None,
                  norm=None, cb_labelpad=10, cb_nticks=10, cb_x=None, cb_y=None,
                  cb_title=None, cb_length=0.75, cb_outlinecolor=None, cb_outlinewidth=1, cb_tickfontsize=10,
                  plot_title='Airstream', title_bold=False, title_size=20, title_pad=5, title_y=0.85,
                  x_label='x', xaxis_bold=False, xaxis_labelpad=5, xlabel_rotation=None, x_tick_number=10,
                  y_label='y', yaxis_bold=False, yaxis_labelpad=5, ylabel_rotation=None, y_tick_number=10,
                  z_label='z', zaxis_bold=False, zaxis_labelpad=5, zlabel_rotation=None, z_tick_number=10,
                  axis_label_size=20, tick_color=None, tick_label_size=12, tick_label_pad=5,
                  xtick_rotation=None, ytick_rotation=None, ztick_rotation=None,
                  floating_text=None, cmap=ColorMaps().mpl_cmap_to_plotly('RdBu'),
                  filename=None,
                  more_subplots_left=False,
                  cb_vmax=None,
                  cb_vmin=None):

        # Colorbar parameters
        self.cb_outlinecolor = cb_outlinecolor if cb_outlinecolor is not None else self.color2
        self.cb_outlinewidth = cb_outlinewidth
        self.cb_length = cb_length
        self.cb_title = cb_title
        self.cb_x = cb_x
        self.cb_y = cb_y
        self.cb_xpad = cb_labelpad
        self.cb_nticks = cb_nticks
        self.cb_tickfontsize = cb_tickfontsize

        # Mock plot
        if isinstance(x, type(None)) and isinstance(y, type(None)) and isinstance(z, type(None)) and isinstance(c, type(None)):
            x = np.linspace(0, 20, 100)
            y = np.linspace(0, 20, 100)
            x, y = np.meshgrid(x, y)
            z = np.arctan2(x, y)
            c = x+y

        # Data
        data = [go.Scatter3d(
                x=x.flatten(),
                y=y.flatten(),
                z=z.flatten(),
                mode='markers',
                marker=dict(size=pointsize,
                            color=c.flatten(),  # set color to an array/list of desired values
                            colorscale=cmap,  # choose a colorscale
                            opacity=opacity,
                            symbol=symbol,
                            colorbar=dict(len=self.cb_length,
                                          x=self.cb_x,
                                          xpad=self.cb_xpad,
                                          y=self.cb_y,
                                          outlinecolor=self.cb_outlinecolor,
                                          outlinewidth=self.cb_outlinewidth,
                                          tick0=0,
                                          dtick=0.5,
                                          ticklen=5,
                                          tickwidth=1,
                                          tickfont=dict(size=self.cb_tickfontsize,
                                                        color=self.color,
                                                        family=self.font
                                                        ),
                                          title=self.cb_title,
                                          nticks=cb_nticks,
                                          tickmode='auto'),
                            cmax=cb_vmax,
                            cmin=cb_vmin
                            ),
                )
                ]

        # Individual axis setup
        axis = dict(showbackground=True,
                    backgroundcolor=pane_fill,
                    showgrid=grid,
                    gridcolor=self.color2,
                    zerolinecolor=self.color2,
                    tickfont={'family': self.font,
                              'size': tick_label_size,
                              'color': tick_color},
                    titlefont={'family': self.font,
                               'size': axis_label_size},
                    )

        # Layout
        layout = go.Layout(
            width=w,
            height=h,
            scene=dict(xaxis=dict(axis, range=x_lim, tickangle=xtick_rotation, nticks=x_tick_number, title='<b>'+x_label+'</b>' if xaxis_bold is True else x_label),
                       yaxis=dict(axis, range=y_lim, tickangle=ytick_rotation, nticks=y_tick_number, title='<b>'+y_label+'</b>' if yaxis_bold is True else y_label),
                       zaxis=dict(axis, range=z_lim, tickangle=ztick_rotation, nticks=z_tick_number, title='<b>'+z_label+'</b>' if zaxis_bold is True else z_label),
                       aspectratio=dict(x=x_scale, y=y_scale, z=z_scale)
                       ),
            template=self.template,
        )

        # Plot
        if isinstance(fig, type(None)):
            fig = go.Figure(data=data, layout=layout)
        else:
            # df = pd.DataFrame(np.random.randint(0, 100, size=(100, 3)), columns=list('xyz'))
            # x = df['x']
            # y = df['y']
            # z = df['z']
            fig.add_trace(go.Scatter3d(x=x.flatten(), y=y.flatten(), z=z.flatten(),
                                       mode="markers",
                                       marker=dict(size=pointsize,
                                                   color=c.flatten(),
                                                   symbol=symbol,
                                                   opacity=opacity,
                                                   colorscale=cmap,
                                                   # colorbar=dict(len=self.cb_length,
                                                   #               x=self.cb_x,
                                                   #               xpad=self.cb_xpad,
                                                   #               y=self.cb_y,
                                                   #               outlinecolor=self.cb_outlinecolor,
                                                   #               outlinewidth=self.cb_outlinewidth,
                                                   #               tick0=0,
                                                   #               dtick=0.5,
                                                   #               ticklen=5,
                                                   #               tickwidth=1,
                                                   #               tickfont=dict(size=self.cb_tickfontsize,
                                                   #                             color=self.color,
                                                   #                             family=self.font),
                                                   #               title=self.cb_title),
                                                   #               nticks=cb_nticks
                                                   cmax=cb_vmax,
                                                   cmin=cb_vmin
                                                   ),
                                       ))

        # Makeup
        fig.update_layout(
            title={'text': '<b>'+plot_title+'<b>' if title_bold is True else plot_title,
                   'x': 0.5,
                   'y': title_y,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(
                family=self.font,
                size=title_size,
                color=self.color,
            ),
            showlegend=showlegend
        )

        if more_subplots_left is False:
            fig.show()

        if not isinstance(filename, type(None)):
            self.save(fig=fig, filename=filename)

        return fig

    def save(self, fig, filename):
        fig.write_image("{}.svg".format(filename))

