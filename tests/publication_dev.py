import numpy as np

import matplotlib.pyplot as plt

from mpl_plotter.setup import figure
from mpl_plotter.color.schemes import one
from mpl_plotter.presets.publication.two_d import line

x = np.linspace(0, 2*np.pi, 100000)
u = np.sin(x)
v = np.cos(x)
y = np.tan(x)
z = np.tanh(x)

fig = figure((20, 4))
ax0 = plt.subplot2grid((1, 4), (0, 0), rowspan=1, colspan=1)
ax1 = plt.subplot2grid((1, 4), (0, 1), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((1, 4), (0, 2), rowspan=1, colspan=1)
ax3 = plt.subplot2grid((1, 4), (0, 3), rowspan=1, colspan=1)

line(x, u, ax=ax0, fig=fig, color=one()[0], x_label="[m]", y_label="$sin (x)$", plot_label="sin")
line(x, v, ax=ax1, fig=fig, color=one()[1], x_label="[m]", y_label="$cos (x)$", plot_label="cos")
line(x, y, ax=ax2, fig=fig, color=one()[2], x_label="[m]", y_label="$tan (x)$", plot_label="tan",
     y_bounds=[-1, 1], fine_tick_locations=False, demo_pad_plot=False)
line(x, z, ax=ax3, fig=fig, color=one()[3], x_label="[m]", y_label="$tanh(x)$",  plot_label="tanh",
     legend=True, legend_loc=(0.925, 0.45))

plt.tight_layout()
plt.show()
