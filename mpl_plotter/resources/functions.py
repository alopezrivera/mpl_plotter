import numpy as np
from matplotlib import colors
from termcolor import colored


def normalize(variant, array, norm):
    if variant == 'SymLog':
        vmin = float(array.min())
        temp = 0

        # Temp raise plot to normalize
        if vmin < 0:
            array = array - vmin
            temp = vmin

        vmax = float(array.max())
        vmin = norm * vmax

        # Revert to original position
        vmax = vmax + temp
        vmin = vmin + temp

        norm = colors.SymLogNorm(linthresh=0.03, linscale=0.03, vmin=vmin, vmax=vmax)

        return norm

    if variant == 'MidPoint':
        vmin = float(array.min())
        vmax = float(array.max())

        range = abs(vmax) + abs(vmin)

        vcenter = vmin + range * norm

        x, y = [vmin, 0.01, vmax], [0, 0.5, 1]
        norm = np.ma.masked_array(np.interp(1, x, y))

        return norm

    if variant == 'Power':
        return colors.PowerNorm(gamma=norm)


def print_color(text, color):
    print(colored('{}'.format(text), color))

