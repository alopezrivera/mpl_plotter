# SPDX-FileCopyrightText: © Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Composition: ``comparison``
---------------------------
"""

import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_plotter.two_d import line
from mpl_plotter.color.schemes import colorscheme_one

from mpl_plotter.utils import tmp


def comparison(x,
               y,
               f=None,
               show=False,
               autocolor=True,
               top=None,
               bottom=None,
               left=None,
               right=None,
               wspace=None,
               hspace=None,
               **kwargs):
    """
    .. raw:: latex

        \subsection*{Data Input}

    The table below displays the supported numerical input combinations, where:

    - array:  List or NumPy array with numerical values
    - [...]:  List containing ...
    - result: <curves>

    .. list-table:: Valid input combinations.
        :widths: 25 25 10 40
        :header-rows: 1

        * - ``x``
          - ``y``
          - Result
          - Notes
        * - array
          - array
          - 1
          - 
        * - array
          - [array, array]
          - 2
          - Both ``y`` share a single ``x``
        * - [array, array]
          - [array, array]
          - 2
          - Both ``x`` share a single ``y``
        * - [n*[array]]
          - [n*[array]]
          - n
          - Each ``y`` has an ``x``

    .. raw:: latex

        \subsubsection*{Argument Classification}
    
    Arguments are internally classified as **figure**, **plural** and **curve** arguments, namely:

    * Figure

      Select few arguments which may be input only once in the plotting process, so as
      to avoid conflicts. Ieg: passing ``grid=True`` twice (``plt.grid(...)``) will result
      in no grid being drawn.
      These are removed from the keyword arguments and used in the last `comparison` call.

    * Plural

      Arguments passed with any of the keywords accepted by all 2D plotters -that is, any keyword
      which does **not** start with the name of its plotting class-, in plural tense.
      These must be **lists** of length equal to the **number of curves**.
      Each element in the list is the value of the keyword argument for each curve (eg: 
      passing ``colors=['red', 'green', 'blue']`` to a 3-curve plot will set the color of the curves 
      to 'red', 'green' and 'blue'.

    * Curve
    
      Curve-specific parameters (``color``, ``line_width``, ``plot_label``)

    .. raw:: latex

        \subsubsection*{Defaults}

    The limits of the plot will be adjusted to the upper and lower limits
    of all ``x``s and ``y``s.

    **Arguments**

    :param x:         Domains.
    :param y:         Values.
    :param f:         Functions used to plot y(x)
    :param autocolor: Whether to automatically assign different colors to each curve
    :param show:      plt.show() after plotting (thereby finishing the plot)
    :param top:       plt.subplots_adjust parameter
    :param bottom:    plt.subplots_adjust parameter
    :param left:      plt.subplots_adjust parameter
    :param right:     plt.subplots_adjust parameter
    :param wspace:    plt.subplots_adjust parameter
    :param hspace:    plt.subplots_adjust parameter
    :param kwargs:    MPL Plotter plotting class keyword arguments for further customization
 
    :type x:          list of list or list of np.ndarray
    :type y:          list of list or list of np.ndarray
    :type f:          list of plot
    :type autocolor:  bool
    :type show:       bool
    :type top:        float
    :type bottom:     float
    :type left:       float
    :type right:      float
    :type wspace:     float
    :type hspace:     float
    """

    ###############################
    #       INPUT VALIDATION      #
    ###############################
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


    ###############################
    #          ARGUMENTS          #
    ###############################
    # figure ----------------------------------------------------------
    fig_par = [                                                         # Get figure specific parameters
                'backend',
                'show',
                'legend',
                'legend_loc',
                'resize_axes',
                'grid'
              ]
    fargs = list(set(fig_par) & set(list(kwargs.keys())))             # Intersection of kwarg keys and fig args
    fargs = {k: kwargs.pop(k) for k in fargs}                       # Dictionary of figure parameters

    # plural ----------------------------------------------------------
    args    = line.__init__.__code__.co_varnames                        # Get line function arguments

    ax_arg = lambda arg: arg[-2:] in ['_x', '_y']

    plurals = [arg + 's' if not ax_arg(arg) else arg[:-2] + 's' + arg[-2:] for arg in args]

    plurals = list(set(plurals) & set(kwargs.keys()))                   # Intersection of kwargs keys and plurals
    plurals = {k: kwargs.pop(k) for k in plurals}                       # Dictionary of plurals

    def plural(i):
        """
        Get plural arguments of the ith curve.

        :param i: index
        """

        _args = {}

        for k in plurals.keys():
            _k = k[:-3] + k[-2:] if ax_arg(k) else k[:-1]
            _args[_k] = plurals[k][i]

        return _args

    # curve -----------------------------------------------------------
    crv_par = [                                                       # Get curve specific parameters
                'color',
                'line_width',
                'plot_label'
              ]
    cargs = list(set(crv_par) & set(list(kwargs.keys())))             # Intersection of kwarg keys and fig args
    cargs = {k: kwargs.pop(k) for k in cargs}                         # Dictionary of figure parameters

    def cparam(i):
        """
        Get curve parameters of the ith curve.

        :param i: index
        """
        cparam = {}
        for k in list(cargs.keys()):
            if isinstance(cargs[k], list):
                cparam[k] = cargs[k][i]
            else:
                cparam[k] = cargs[k]
        return cparam

    ###############################
    #          DEFAULTS           #
    ###############################
    # Plot defaults
    fargs['backend']    = fargs.pop('backend',    'Qt5Agg')
    fargs['legend']     = fargs.pop('legend',     'plot_labels' in plurals.keys() or 'plot_label' in kwargs.keys())
    fargs['legend_loc'] = fargs.pop('legend_loc', (0.815, 0.4925))

    if 'color' not in cargs.keys() and 'colors' not in plurals.keys() and autocolor:
        cargs['color'] = colorscheme_one()

    ###############################
    #           LIMITS            #
    ###############################
    y_max = max(y[n].max() for n in range(len(y)))
    y_min = min(y[n].min() for n in range(len(y)))
    span_y = abs(y_max - y_min)

    x_max = max(x[n].max() for n in range(len(x)))
    x_min = min(x[n].min() for n in range(len(x)))
    span_x = abs(x_max - x_min)

    bounds_x      = kwargs.pop('bounds_x',      [x_min - 0.05 * span_x, x_max + 0.05 * span_x])
    bounds_y      = kwargs.pop('bounds_y',      [y_min - 0.05 * span_y, y_max + 0.05 * span_y])
    tick_bounds_x = kwargs.pop('tick_bounds_x', [x_min, x_max])
    tick_bounds_y = kwargs.pop('tick_bounds_y', [y_min, y_max])    

    ###############################
    #           FIGURE            #
    ###############################
    n_curves = len(y) if not single_y else len(x) if not single_x else 1
    f        = f if isinstance(f, list) else [f]*n_curves if f is not None else [line]*n_curves

    ###############################
    #            PLOT             #
    ###############################
    for n in range(n_curves):

        args = {**kwargs, **plural(n), **cparam(n)} if n != n_curves - 1 else {**kwargs, **plural(n), **cparam(n), **fargs}

        f[n](x=x[n] if not single_x else x,
             y=y[n] if not single_y else y,
             
             bounds_x=bounds_x,
             bounds_y=bounds_y,
             
             tick_bounds_x=tick_bounds_x,
             tick_bounds_y=tick_bounds_y,
             
             resize_axes=kwargs.pop('resize_axes', True) if n == n_curves - 1 else False,   # Avoid conflict
             grid=kwargs.pop('grid', True) if n == n_curves - 1 else False,                 # Avoid conflict
             
             **args,
             )

    # Margins
    plt.subplots_adjust(top=     0.95                             if top    is None else top,
                        bottom=  0.11                             if bottom is None else bottom,
                        left=    0.05                             if left   is None else left,
                        right=   0.85                             if right  is None else right,
                        wspace=  0.35                             if wspace is None else wspace,
                        hspace=  0.6                              if hspace is None else hspace)

    if fargs['legend']:
        # Legend placement
        legend = (c for c in plt.gca().get_children() if isinstance(c, mpl.legend.Legend))

        plt.savefig(os.path.join(tmp(), 'tmp.pdf'),
                    bbox_extra_artists=legend,      # Expand figure to fit legend
                    )

    if show:
        plt.show()
