from mpl_plotter import figure
from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area
from mpl_plotter.three_d import line as l3, scatter as s3, surface

import matplotlib.pyplot as plt

fig = figure(figsize=(15, 15))

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
         lambda *args, **kwargs: l3(azim=-159, elev=41, *args, **kwargs),
         lambda *args, **kwargs: s3(azim=-159, elev=41, *args, **kwargs),
         lambda *args, **kwargs: surface(azim=-159, elev=41, *args, **kwargs)]

for i in range(len(plots)):
    plots[i](fig=fig, ax=axes[i])

plt.subplots_adjust(top=0.895,
                    bottom=0.11,
                    left=0.08,
                    right=0.94,
                    hspace=0.245,
                    wspace=0.25)

plt.savefig('../gallery/showcase/demo.png', dpi=200)
plt.show()
