"""
Antonio Lopez Rivera, 2020
"""

from mpl_plotter.three_d import surface

surface(figsize=(7, 7),
        azim=-133, elev=43,

        show_axes=False, grid=False,
        background_color_figure="black", background_color_plot="black",

        surface_alpha=0, 
        surface_edge_color="white", 
        surface_wire_width=0.5,
        surface_rstride=8, surface_cstride=100,

        top=0.925,
        bottom=0.085,
        left=0.035,
        right=0.905,
        hspace=0.2,
        wspace=0.2,

        show=True)
