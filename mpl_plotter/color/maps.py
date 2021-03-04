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