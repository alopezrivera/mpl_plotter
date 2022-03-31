# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Color Maps
----------
"""


from matplotlib.colors import LinearSegmentedColormap


def custom(red, green, blue,
           name="coolheat", n=1024):
    """
    :param red: List of (red fraction, y0, y1) tuples
    :param green: List of (red fraction, y0, y1)
    :param blue: List of (red fraction, y0, y1)
    :param name: Colormap name
    :param n: RBG quantization levels
    :return: Colormap
    """
    dictionary = {
        'red': red,
        'green': green,
        'blue': blue}
    return LinearSegmentedColormap(name, dictionary, n)


def mapstack(maps,
             fractions=None,
             ranges=None):
    """
    Create a colormap stacking an arbitrary number of
    conventional Matplotlib colormaps.

    :param maps:      List of colormap NAMES
    :param fractions: For each original colormap, the fraction it'll take of the merged colormap.
                         [0<fr_0<1, ...]
    :param ranges:    For each original colormap, the range taken.
                         [(0=<min<1, 0<max<=1)_0, ...]

    :type maps:       list of str
    :type fractions:  list of float
    :type ranges:     list of tuple

    :return: mpl.colors.LinearSegmentedColormap
    """

    if fractions is None:
        fractions = np.ones(len(maps))*1/len(maps)

    if ranges is None:
        ranges = np.tile(np.array([0, 1]), (len(maps), 1))

    stack = tuple(mpl.cm.get_cmap(maps[i])(np.linspace(ranges[i][0], ranges[i][1], int(round(256 * fractions[i], 0))))
                  for i in range(len(maps)))

    colors = np.vstack(stack)

    return mpl.colors.LinearSegmentedColormap.from_list('custom_RdBu', colors)
