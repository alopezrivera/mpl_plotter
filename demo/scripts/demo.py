from mpl_plotter import figure
from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area
from mpl_plotter.three_d import line as l3, scatter as s3, surface

import matplotlib.pyplot as plt

fig = figure(figsize=(9, 8))

ax0 = plt.subplot2grid((3, 3), (0, 0), rowspan=1, fig=fig)
ax1 = plt.subplot2grid((3, 3), (0, 1), rowspan=1, fig=fig)
ax2 = plt.subplot2grid((3, 3), (0, 2), rowspan=1, fig=fig)
ax3 = plt.subplot2grid((3, 3), (1, 0), rowspan=1, fig=fig)
ax4 = plt.subplot2grid((3, 3), (1, 1), rowspan=1, fig=fig)
ax5 = plt.subplot2grid((3, 3), (1, 2), rowspan=1, fig=fig)
ax6 = plt.subplot2grid((3, 3), (2, 0), rowspan=1, fig=fig, projection='3d')
ax7 = plt.subplot2grid((3, 3), (2, 1), rowspan=1, fig=fig, projection='3d')
ax8 = plt.subplot2grid((3, 3), (2, 2), rowspan=1, fig=fig, projection='3d')

axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
plots = [line, scatter, heatmap, quiver, streamline, fill_area,
         lambda *args, **kwargs: l3(azim=-159, elev=41, *args, **kwargs,
                                    ),
         lambda *args, **kwargs: s3(azim=-159, elev=41, *args, **kwargs,
                                    title_size=110,
                                    title_weight="bold",
                                    title_font="Pump Triline",
                                    title_color="black",
                                    title_y=3.75,
                                    ),
         lambda *args, **kwargs: surface(azim=-159, elev=41, *args, **kwargs,
                                         surface_rstride=5,
                                         surface_cstride=10,
                                         surface_wire_width=0.5,
                                         surface_edge_color='black',
                                         surface_alpha=0,
                                         top=0.95,
                                         bottom=0.1,
                                         left=0.1,
                                         right=0.94,
                                         hspace=0.245,
                                         wspace=0.5)]

for i in range(len(plots)):

    kwargs = {
        "fig":           fig,
        "ax":            axes[i],
        "tick_number_x": i+1 if i+1 <= 5 else (9-i),  
        "tick_number_y": i+1 if i+1 <= 5 else (9-i),
    }

    if i > 5:
        kwargs['tick_number_z'] = i+1 if i+1 <= 5 else (9-i)

    plots[i](**kwargs)

plt.savefig('../gallery/showcase/demo.png', dpi=200)

plt.show()
