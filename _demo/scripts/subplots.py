from mpl_plotter import figure
from mpl_plotter.two_d import line, scatter, heatmap, quiver, streamline, fill_area

import matplotlib.pyplot as plt

fig = figure(figsize=(15, 10))

ax0 = plt.subplot2grid((2, 3), (0, 0), rowspan=1, fig=fig)
ax1 = plt.subplot2grid((2, 3), (0, 1), rowspan=1, fig=fig)
ax2 = plt.subplot2grid((2, 3), (0, 2), rowspan=1, fig=fig)
ax3 = plt.subplot2grid((2, 3), (1, 0), rowspan=1, fig=fig)
ax4 = plt.subplot2grid((2, 3), (1, 1), rowspan=1, fig=fig)
ax5 = plt.subplot2grid((2, 3), (1, 2), rowspan=1, fig=fig)

axes = [ax0, ax1, ax2, ax3, ax4, ax5]
plots = [line, scatter, heatmap, quiver, streamline, fill_area]

for i in range(len(plots)):
    plots[i](fig=fig, ax=axes[i])

plt.subplots_adjust(top=0.895,
                    bottom=0.11,
                    left=0.08,
                    right=0.94,
                    hspace=0.245,
                    wspace=0.25)

plt.show()
