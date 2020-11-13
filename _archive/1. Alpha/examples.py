import numpy as np
import pandas as pd

from matplotlib import cm
from numpy import sin, cos

from mpl_plotting_methods import MatPlotLibPublicationPlotter as mplPlotter
from mock_data import MockData
from data_input import Data2D, Data3D
from ply_plotting_methods import PlotLyPublicationPlotter

"""
Examples
"""


def heatmap_test(julia=False):
    if julia is True:
        data = MockData().filled_julia(df=True)
    else:
        data = None
    ax = mplPlotter(light=True).heatmap(array=data,
                                        plot_title='Look at that title',
                                        color_bar=True, cb_nticks=22)
    mplPlotter(light=True, ax=ax).floating_text2d(x=-100, y=75,
                                                  text='Max Force = 2976 N',
                                                  size=17, weight='bold', color='white')
    mplPlotter(light=True, ax=ax).floating_text2d(x=0.8, y=30,
                                                  text='(0.8, 30 [m/s]) => 1000N',
                                                  size=11, weight='normal', color='white')


def plot2d_test():
    fig = mplPlotter(light=True).setup2d(figsize=(6, 10))
    # Demo spirograph
    ax1 = mplPlotter(light=True, fig=fig, shape_and_position=211).plot2d(grid=True, resize_axes=False, more_subplots_left=True)
    # Extra plot
    x, y = MockData().sinewave()
    ax2 = mplPlotter(light=True, fig=fig, shape_and_position=212).plot2d(x=x, y=y,
                                                                         plot_title=r"$f(x) = \int_{0}^{x} -cos(x)$", title_size=13, title_bold=True, title_y=1.15)
    # Floating text
    mplPlotter(light=True, fig=fig, ax=ax1).floating_text2d(x=-100, y=75, text='Max Force = 2976 N',
                                                            size=17, weight='bold')
    mplPlotter(light=True, fig=fig, ax=ax2).floating_text2d(x=0.8, y=30, text='(0.8, 30 [m/s]) => 1000N',
                                                            size=11, weight='normal')


def custom_subplots_test():
    # Subplot setup
    widths = [4, 1]
    heights = [1]
    fig, axes = mplPlotter(light=True).custom_subplots(widths=widths, heights=heights, ncols=2, nrows=1)
    # Demo spirograph
    mplPlotter(light=True, fig=fig, ax=axes[0], shape_and_position=211).plot2d(custom_subplots=True,
                                                                               grid=True,
                                                                               plot_title='Spirograph',
                                                                               more_subplots_left=True)
    # Extra plot
    x, y = MockData().sinewave()
    mplPlotter(light=True, fig=fig, ax=axes[1], shape_and_position=212).plot2d(custom_subplots=True,
                                                                               # grid already drawn
                                                                               x=x, y=y,
                                                                               plot_title=r"$f(x) = \int_{0}^{x} -cos(x)$", title_size=15, title_bold=True, title_y=1.1,
                                                                               more_subplots_left=False)
    # Floating text
    mplPlotter(light=True, fig=fig, ax=axes[0]).floating_text2d(x=-100, y=75,
                                                                text='Max Force = 2976 N',
                                                                size=17, weight='bold')
    mplPlotter(light=True, fig=fig, ax=axes[1]).floating_text2d(x=0.8, y=30,
                                                                text='(0.8, 30 [m/s]) => 1000N',
                                                                size=11, weight='normal')


def surface3d_test():
    fig = mplPlotter().setup3d(figsize=(10, 5))
    mplPlotter(light=True, fig=fig, shape_and_position=111).surface3d(cstride=2, rstride=2,
                                                                      x_scale=5, y_scale=5,
                                                                      z_tick_number=2)


def tricontour_test():
    mplPlotter().tricontour(cb_labelpad=2, cb_nticks=6, plot_title='Random distribution')


def isosurface_test():
    mplPlotter().isosurface(plot_title=r"$f(x, y, z) = cos(x) + cos(y) + cos(z) - $ \TeX $ = \int_{a}^{b} \Delta^2$")


def hill_shades_test():
    fig = mplPlotter().setup3d(figsize=(7, 10))
    x = MockData().hill()[0]
    y = MockData().hill()[1]
    z = MockData().hill()[2]
    mplPlotter(fig=fig, shape_and_position=221).surface3d(x=x, y=y, z=z, lighting=True,
                                                          plot_title=r"Big ass mountain hill ain't that right \TeX",
                                                          cmap=cm.get_cmap('gist_earth'), grid=True, more_subplots_left=True)
    mplPlotter(fig=fig, shape_and_position=222).surface3d(x=x, y=y, z=z, lighting=True,
                                                          plot_title=r"Big ass mountain hill ain't that right \TeX",
                                                          cmap=cm.get_cmap('gist_earth'), grid=True, more_subplots_left=True)
    mplPlotter(fig=fig, shape_and_position=223).surface3d(x=x, y=y, z=z, lighting=True,
                                                          plot_title=r"Big ass mountain hill ain't that right \TeX",
                                                          cmap=cm.get_cmap('gist_earth'), grid=True, more_subplots_left=True)
    mplPlotter(fig=fig, shape_and_position=224).surface3d(x=x, y=y, z=z, lighting=True,
                                                          plot_title=r"Big ass mountain hill ain't that right \TeX",
                                                          cmap=cm.get_cmap('gist_earth'), grid=True)


def plane_intersection_test():
    PlotLyPublicationPlotter().intersection3d()


def volume_test():
    PlotLyPublicationPlotter().volume()


# To use Latex it is extremely important to have an updated version of MikTex
#    - Download MikTex Console
#    - Add MikTex to PATH -usually automatic in Windows
#    - It is iffy, be patient


def data_input_line2d_test():
    def f(x):
        return 2*x
    x, y = Data2D().line(f=f, u0=0, un=10, n=50)
    mplPlotter(light=True).plot2d(x=x, y=y, resize_axes=False,
                                  plot_title='Graph of $f(x)=2x$', title_size=13, xaxis_bold=True,
                                  tick_color='red',
                                  grid=True, gridcolor='red', gridlines='dotted')


def data_input_heatmap_test():
    def f(x, y):
        return np.exp(x+y)
    z = Data2D().heatmap(f=f, u0=0, un=10, v0=0, vn=10, n=50)
    mplPlotter(light=True).heatmap(array=z, resize_axes=True,
                                   plot_title='Graph of $f(x, y)=e^{x+y}$', title_size=13, xaxis_bold=True,
                                   tick_color='red',
                                   grid=True, gridcolor='red', gridlines='dotted',
                                   tick_ndecimals=1, x_tick_number=11, y_tick_number=11)


def data_input_line3d_test():
    def f(x):
        return sin(x)
    def g(x):
        return cos(x)
    x, y, z = Data3D().line(f=f, g=g, u0=0, un=10, n=50)
    mplPlotter(light=True).line3d(x=x, y=y, z=z, linewidth=10, plot_title='$y = sin(x)$ \n $z = cos(x)$')


def data_input_surface_test():
    def f(x, y):
        return x*x + y*y
    x, y, z = Data3D().surface(f=f, u0=-5, un=5, v0=-5, vn=5, n=50)
    mplPlotter(light=True).surface3d(x=x, y=y, z=z, plot_title='$f(x, y) = x^2 + y^2$', cmap='gnuplot')


def data_input_trisurf_test():
    def f(x, y):
        return (1 + 0.5 * y * np.cos(x / 2.0)) * np.cos(x)
    def g(x, y):
        return (1 + 0.5 * y * np.cos(x / 2.0)) * np.sin(x)
    def h(x, y):
        return 0.5 * y * sin(x / 2.0)
    x, y, z, tri = Data3D().triangular_mesh(u0=0, un=2.0 * np.pi, v0=-0.5, vn=0.5, f=f, g=g, h=h, n=50)
    mplPlotter().isosurface(x=x, y=y, z=z, triangles=tri, cmap='Spectral', plot_title='Mobius strip in x(u, v), y(u, v), z(u, v) coordinates \n'
                                                                                      '- triangulated with mplPlotter.isosurface()')


def data_input_3dvector_test():
    def rule(u, v, w):
        return np.arctan2(u, v)

    df = pd.read_csv(
        r"C:\Users\xXY4n\AE BSc\AE Year 2\Aerodynamics project\Data Analysis\data\velocity_planes_of_interest\x=-10\x=-10_projected\-10_-8_7.csv"
    )
    df.columns = list('---xyzuvw')
    x = df['x']
    y = df['y']
    z = df['z']
    u = df['u']
    v = df['v']
    w = df['w']

    mplPlotter(usetex=False).vectors3D(x=x, y=y, z=z, u=u, v=v, w=w, resize_axes=False, cmap='copper',
                                       plot_title=r'Projection onto the x=-10 plane of the -10_-8_7 bin',
                                       vectorlength=0.075, vectorwidth=3, rule=rule)


def data_input_2dvector_test():
    def rule(u, v):
        return np.arctan2(u, v)

    df = pd.read_csv(
        r"C:\Users\xXY4n\AE BSc\AE Year 2\Aerodynamics project\Data Analysis\data\velocity_planes_of_interest\x=-10\x=-10_projected\-10_-8_7.csv"
    )
    df.columns = list('---xyzuvw')
    x = df['x']
    y = df['y']
    z = df['z']
    u = df['u']
    v = df['v']
    w = df['w']

    mplPlotter(usetex=False).vectors2d(x=x, y=y, u=u, v=v, resize_axes=False, cmap='copper',
                                       plot_title=r'Projection onto the x=-10 plane of the -10_-8_7 bin',
                                       rule=rule)
data_input_surface_test()
