"""
Antonio Lopez Rivera, 2020
"""

from mpl_plotter.three_d import surface

surface(show=True, alpha=0, edge_color="white", line_width=0.5,
        show_axes=False, grid=False,
        azim=-133, elev=43,
        rstride=8, cstride=100,
        figsize=(7, 7), background_color_figure="black", background_color_plot="black")
