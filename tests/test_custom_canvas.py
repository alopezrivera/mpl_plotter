import numpy as np
import matplotlib.pyplot as plt
from mpl_plotter.setup import custom_canvas

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

c = custom_canvas(x=x, y=y, spines_removed=None, font_color="darkred")
ax, fig = c.ax, c.fig


plt.plot(x, y)

plt.show()
