import matplotlib.pyplot as plt

from mpl_plotter.setup import figure
from mpl_plotter.two_d import line, quiver, heatmap, streamline
from mpl_plotter.three_d import surface


def subplot2grid():

    fig = figure((18, 8))

    ax1 = plt.subplot2grid((2, 6), (0, 0), colspan=2, rowspan=2, projection='3d')
    ax2 = plt.subplot2grid((2, 6), (0, 3), rowspan=1, aspect=1)
    ax3 = plt.subplot2grid((2, 6), (1, 3), rowspan=1, aspect=1)
    ax4 = plt.subplot2grid((2, 6), (0, 5), rowspan=1, aspect=1)
    ax5 = plt.subplot2grid((2, 6), (1, 5), rowspan=1, aspect=1)

    surface(fig=fig, ax=ax1, more_subplots_left=True)
    line(fig=fig, ax=ax2, more_subplots_left=True)
    quiver(fig=fig, ax=ax3, more_subplots_left=True)
    heatmap(fig=fig, ax=ax4, more_subplots_left=True)
    streamline(fig=fig, ax=ax5, more_subplots_left=True)

    plt.savefig(r"C:\Users\xXY4n\Programming_projects\Non-embedded\Python\mpl_plotter\_demo\subplot2grid_demo.png",
                dpi=150)
    plt.show()


subplot2grid()
