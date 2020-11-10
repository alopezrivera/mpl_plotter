import numpy as np

from resources.mock_data import MockData
from two_d import fill_area, line

x = np.arange(-6, 6, .01)
y = np.sin(x)
z = np.sin(x-45/180*np.pi)

line(x, y, more_subplots_left=True)
line(x, z, more_subplots_left=True)
fill_area(x=x, y=y, z=z, above=True)
