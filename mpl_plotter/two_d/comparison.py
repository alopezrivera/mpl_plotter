# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Comparison plot method
----------------------
"""

import inspect

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from alexandria.paths import home

from mpl_plotter.two_d import line
from mpl_plotter.color.schemes import colorscheme_one


def comparison(x,
               y,
               f=None,
               show=False,
               top=None,
               bottom=None,
               left=None,
               right=None,
               wspace=None,
               hspace=None,
               **kwargs):
    """
    # Inputs
    The panes function supports numerical inputs in the following forms:
    |   x                      |   y                       |  result  |  notes               |
    |  ---                     |  ---                      |  ---     |  ---                 |
    |  array                   |  array                    |  1       |                      |
    |  array                   |  [array, array]           |  2       |  Both `y`s share `x` |
    |  [array, array]          |  [array, array]           |  2       |  Each `y` has an `x` |
    |  [n*[array]              |  [n*[array]]              |  n       |  Each `y` has an `x` |

    where

    * array:  List or NumPy array with numerical values
    * [...]:  List containing ...
    * result: <curves>

    # Arguments
    Arguments are internally classified as FIGURE arguments, AXIS arguments, PLURAL arguments
    and CURVE arguments, namely:

    * Figure
        Select few arguments which may be input only once in the plotting process, so as
        to avoid conflicts. Ieg: passing `grid=True` twice (`plt.grid(...)`) will result
        in no grid being drawn.
        These are removed from the keyword arguments and used in the last `comparison` call.

    * Plural
        Arguments with a keyword equal to any of the arguments which can be passed to the
          `line`
        2D plotter, in plural tense. The line plotter is chosen as it shares all general
        arguments with the other 2D plotter functions.
        The plural arguments are assumed to be
          `lists of length equal to the number of curves`
        and thus modify each curve. Ieg: colors=['red', 'green', 'blue'] will set the color
        of each curve to 'red', 'green' and 'blue' respectively in a 3-curve plot.

    * Curve


    # Defaults
    The limits of the plot will be adjusted to the upper and lower limits
    of all `x`s and `y`s.

    :param x:               Domains.
    :param y:               Values.
    :param f:               Functions used to plot y(x)
    :param kwargs:          MPL Plotter plotting class keyword arguments for further customization

    :type x:                list of list or list of np.ndarray
    :type y:                list of list or list of np.ndarray
    :type f:                list of plot
    """

    # Figure arguments
    fig_par = [                                                         # Get figure specific parameters
                'backend',
                'show',
                'legend',
                'legend_loc',
                'resize_axes',
                'grid'
              ]
    fparams = list(set(fig_par) & set(list(kwargs.keys())))             # Intersection of kwarg keys and fig params
    fparams = {k: kwargs.pop(k) for k in fparams}                       # Dictionary of figure parameters

    # Plurals
    params = list(dict(inspect.signature(line).parameters).keys())      # Get line function parameters
    plurals = [param + 's' for param in params]                         # Parameters: in plural
    plurals = list(set(plurals) & set(list(kwargs.keys())))             # Intersection of kwargs keys and plurals
    plurals = {k: kwargs.pop(k) for k in plurals}                       # Dictionary of plurals

    def plural(i):
        """
        Get plural parameters of the ith curve.

        :param i: index
        """
        try:
            return {k[:-1]: plurals[k][i] for k in list(plurals.keys())}
        except TypeError:
            print(plurals, i)

    # Curve parameters
    crv_par = [                                                         # Get curve specific parameters
                'color',
                'line_width',
                'plot_label'
              ]
    cparams = list(set(crv_par) & set(list(kwargs.keys())))             # Intersection of kwarg keys and fig params
    cparams = {k: kwargs.pop(k) for k in cparams}                       # Dictionary of figure parameters

    def cparam(i):
        """
        Get curve parameters of the ith curve.

        :param i: index
        """
        cparam = {}
        for k in list(cparams.keys()):
            if isinstance(cparams[k], list):
                cparam[k] = cparams[k][i]
            else:
                cparam[k] = cparams[k]
        return cparam

    # Plot defaults
    fparams['backend']    = fparams.pop('backend',    'Qt5Agg')
    fparams['legend']     = fparams.pop('legend',     'plot_labels' in plurals.keys() or 'plot_label' in kwargs.keys())
    fparams['legend_loc'] = fparams.pop('legend_loc', (0.7, 0.675))

    if 'color' not in cparams.keys() and 'colors' not in plurals.keys():
        cparams['color'] = colorscheme_one()

    # Limits
    y_max = max(y[n].max() for n in range(len(y)))
    y_min = min(y[n].min() for n in range(len(y)))
    span_y = abs(y_max - y_min)

    x_max = max(x[n].max() for n in range(len(x)))
    x_min = min(x[n].min() for n in range(len(x)))
    span_x = abs(x_max - x_min)

    x_bounds = kwargs.pop('x_bounds', [x_min - 0.05 * span_x, x_max + 0.05 * span_x])
    y_bounds = kwargs.pop('y_bounds', [y_min - 0.05 * span_y, y_max + 0.05 * span_y])
    y_custom_tick_locations = kwargs.pop('y_custom_tick_locations', [y_min, y_max])
    x_custom_tick_locations = kwargs.pop('x_custom_tick_locations', [x_min, x_max])

    # Input check
    single_x = (isinstance(x, list) and len(x) == 1) or isinstance(x, np.ndarray)
    single_y = (isinstance(y, list) and len(y) == 1) or isinstance(y, np.ndarray)

    x = np.array(x).squeeze() if single_x else x
    y = np.array(y).squeeze() if single_y else y

    if single_x:
        if single_y:
            if len(x) != len(y):
                raise ValueError('The length of x and y does not match.')
        else:
            assert all([len(curve) == len(x) for curve in y]), ValueError('The length of x and the pairs in y does not match.')
    else:
        if single_y:
            assert all([len(curve) == len(y) for curve in x]), ValueError('The length of y and the pairs in x does not match.')
        else:
            assert len(x) == len(y), ValueError('x, y: size mismatch.')

    # Figure setup
    n_curves = len(y) if not single_y else len(x) if not single_x else 1
    f        = f if isinstance(f, list) else [f]*n_curves if f is not None else [line]*n_curves

    # Plot
    for n in range(n_curves):

        args = {**kwargs, **plural(n), **cparam(n)} if n != n_curves - 1 else {**kwargs, **plural(n), **cparam(n), **fparams}

        f[n](x=x[n] if not single_x else x,
             y=y[n] if not single_y else y,

             x_bounds=x_bounds, y_bounds=y_bounds,
             x_custom_tick_locations=x_custom_tick_locations, y_custom_tick_locations=y_custom_tick_locations,

             resize_axes=kwargs.pop('resize_axes', True) if n == n_curves - 1 else False,   # Avoid conflict
             grid=kwargs.pop('grid', True) if n == n_curves - 1 else False,                 # Avoid conflict

             **args,
             )

    # Margins
    plt.subplots_adjust(top=     1.00                             if top    is None else top,
                        bottom=  0.11                             if bottom is None else bottom,
                        left=    0.1                              if left   is None else left,
                        right=   0.85                             if right  is None else right,
                        wspace=  0.6                              if wspace is None else wspace,
                        hspace=  0.35                             if hspace is None else hspace)


    if fparams['legend']:
        # Legend placement
        legend = (c for c in plt.gca().get_children() if isinstance(c, mpl.legend.Legend))

        plt.savefig(f"{home()}/temp.pdf",
                    bbox_extra_artists=legend,      # Expand figure to fit legend
                    )

    if show:
        plt.show()
