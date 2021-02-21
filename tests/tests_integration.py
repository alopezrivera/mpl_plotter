import numpy as np

import matplotlib.pyplot as plt

from mpl_plotter.setup import figure
from mpl_plotter.customize import customize
from mpl_plotter.two_d import line, quiver, heatmap, streamline, fill_area
from mpl_plotter.three_d import surface


def subplot2grid():

    fig = figure((18, 8))

    ax1 = plt.subplot2grid((2, 6), (0, 0), colspan=2, rowspan=2, projection='3d', facecolor="#fff6e6")
    ax2 = plt.subplot2grid((2, 6), (0, 3), rowspan=1, aspect=1)
    ax3 = plt.subplot2grid((2, 6), (1, 3), rowspan=1, aspect=1)
    ax4 = plt.subplot2grid((2, 6), (0, 5), rowspan=1, aspect=1)
    ax5 = plt.subplot2grid((2, 6), (1, 5), rowspan=1, aspect=1)

    surface(fig=fig, ax=ax1,
            title="Demo",
            title_size=70,
            title_weight="bold",
            title_font="Pump Triline",
            title_color="#e69300",
            plot_label="Surface",
            azim=-160,
            elev=43)
    # line(fig=fig, ax=ax2, color="#ffbf87",
    #      plot_label="Line", grid=True)
    fill_area(fig=fig, ax=ax2, plot_label="Fill", aspect=12)
    quiver(fig=fig, ax=ax3,
           plot_label="Quiver")
    heatmap(fig=fig, ax=ax4,
            title="No label",
            plot_label="Heatmap")
    streamline(fig=fig, ax=ax5,
               title="No label",
               plot_label="Streamline")

    customize(fig=fig, ax=ax2,
              background_color_figure="#fff6e6",
              legend=True, legend_loc=(0.6725, 0.425))

    plt.show()


subplot2grid()
