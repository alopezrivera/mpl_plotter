from mpl_plotter.three_d import surface

import numpy as np

x = np.linspace(0, 20*np.pi, 100)
y = np.sin(x)
x, y = np.meshgrid(x, y)
z = np.cos(x+y)

surface(x=x, y=y, z=z, show=True,
        z_bounds=[-5, 5])
