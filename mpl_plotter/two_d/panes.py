# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Composition: ``panes``
----------------------
"""

import os

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from math import floor, ceil
from copy import deepcopy as dc

from mpl_plotter import figure
from mpl_plotter.two_d import line
from mpl_plotter.two_d.comparison import comparison

from mpl_plotter.utils import tmp


def panes(x,
          y,
          f=None,
          fig=None,
          shape=None,
          figsize=None,
          show=False,
          rows=1,
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
          - 11
          -
        * - array                   
          - [array, array]          
          - 12
          - Both ``y`` share ``x``                         
        * - [n*[array]]             
          - [n*[array]]             
          - 1n
          - Each ``y`` has an ``x``                           
        * - array                   
          - [array, array]          
          - 21
          - Both ``y`` share ``x``                           
        * - [array, array]          
          - [array, array]          
          - 21
          - Each ``y`` has an ``x``                           
        * - array                   
          - [n*[array], n*[array]]  
          - 2n
          - All curves in all (2) panes share a single ``x``
        * - [array, array]          
          - [n*[array], n*[array]]  
          - 2n
          - All curves in each pane share an ``x``          
        * - [n*[array], n*[array]]  
          - [n*[array], n*[array]]  
          - 2n
          - All curves in all (2) panes have their own ``x``
        * - [n*[array], ... up to m]
          - [n*[array], ... up to m]
          - mn
          - All curves in all panes have their own ``x``    

    .. raw:: latex

        \subsubsection*{Argument Classification}
    
    Arguments are internally classified as **figure**, **legend**, **plural** and **curve** arguments, namely:

    * Figure arguments

      Arguments which may be input only once in the plotting process, so as
      to avoid conflicts (eg: passing ``grid=True`` twice (``plt.grid(...)``) will result
      in no grid being drawn). These are removed from the keyword arguments and applied in 
      the last ``comparison`` call.

    * Legend arguments

      These are ``plot_label/s``, which to avoid redundancy are applied in the last ``comparison``. 
      This is done only if the number of curves is the same across all panes, and equal to the number 
      of provided ``plot_labels``.

    * Plural arguments

      Arguments passed with any of the keywords accepted by all 2D plotters -that is, any keyword
      which does **not** start with the name of its plotting class-, in plural tense.
      These must be **lists** of length equal to the **number of panes**.
      Each element in the list is the value of the keyword argument for each pane (eg: 
      ``tick_labels_x=[1, 2, 3]`` will set the tick labels of the x axes to 1, 2 and 3 
      respectively in a 3-pane plot).

    * Curve arguments

      Arguments passed as plurals to the comparison function. These are once more **lists**
      containing the value of a keyword argument, passed in plural, for each curve following
      the convention shown above for data input, such that passing
      ``colors=[['red', 'blue'], ['green', 'red']]`` to a plot containing 2 panes with 2 curves
      each will color the curves in the first pane red and blue, and those in the second green and red.

    **Arguments**
    
    :param x:        Data
    :param y:        Data
    :param f:        List of plotting functions to use for each curve
    :param fig:      Figure object on which to plot
    :param figsize:  Figure size
    :param show:     Whether to plt.show() after plotting (thereby finishing the plot)
    :param rows:     Number of rows
    :param top:      plt.subplots_adjust parameter
    :param bottom:   plt.subplots_adjust parameter
    :param left:     plt.subplots_adjust parameter
    :param right:    plt.subplots_adjust parameter
    :param wspace:   plt.subplots_adjust parameter
    :param hspace:   plt.subplots_adjust parameter
    :param kwargs:   MPL Plotter plotting class keyword arguments for further customization

    :type x:         list of list or list of np.ndarray or np.ndarray
    :type y:         list of list or list of np.ndarray or np.ndarray
    :type f:         list of function or list of plot
    :type fig:       matplotlib.figure.Figure
    :type figsize:   tuple of float
    :type show:      bool
    :type rows:      int
    :type top:       float
    :type bottom:    float
    :type left:      float
    :type right:     float
    :type wspace:    float
    :type hspace:    float

    **Output**

    :param panes:    list of lists, each containing the objects output by each Matplotlib plotting function used
    """

    ###############################
    #       INPUT VALIDATION      #
    ###############################
    single_x = (not isinstance(x[0], list) and len(x) == 1) or isinstance(x, np.ndarray)
    single_y = (not isinstance(y[0], list) and len(y) == 1) or isinstance(y, np.ndarray)

    x = np.array(x).squeeze() if single_x else x
    y = np.array(y).squeeze() if single_y else y

    if single_x:
        if single_y:
            if len(x) != len(y):
                raise ValueError('The length of x and the pairs in y does not match.')
        else:
            if isinstance(y[0], list):
                assert all([len(curve) == len(x) for curve in y[0]]), \
                    ValueError('The length of x and the curves in the pairs of y does not match.')
            else:
                assert all([len(curve) == len(x) for curve in y]), \
                    ValueError('The length of x and the curves in y does not match.')
    else:
        if single_y:
            if isinstance(x[0], list):
                assert all([len(curve) == len(y) for curve in x[0]]), \
                    ValueError('The length of x and the curves in the pairs of y does not match.')
            else:
                assert all([len(curve) == len(y) for curve in x]), \
                    ValueError('The length of x and the curves in y does not match.')

    ###############################
    #         PLOT NUMBER         #
    ###############################
    if not single_y and not single_x:
        if isinstance(y[0], list):
            n_plots = len(y)
        elif isinstance(x[0], list):
            n_plots = len(x)
        else:
            n_plots = len(y)
    elif single_y:
        n_plots = len(x) if not single_x else 1
    elif single_x:
        n_plots = len(y) if not single_y else 1

    ###############################
    #          ARGUMENTS          #
    ###############################
    # keys ------------------------------------------------------------
    fkeys   = [
        'backend',
        'show',
        'legend',
        'legend_loc'
    ]
    lkeys   = [
        'plot_label',
        'plot_labels'
    ]

    # figure arguments ------------------------------------------------
    fargs = {k: kwargs.pop(k) for k in list(set(fkeys) & set(kwargs.keys()))}

    fargs['backend']    = fargs.pop('backend',    'Qt5Agg')
    fargs['legend_loc'] = fargs.pop('legend_loc', (0.875, 0.55))

    # legend arguments -----------------------------------------------
    largs = {k: kwargs.pop(k) for k in dc(kwargs).keys() if k in lkeys and len([kwargs[k]] if not isinstance(kwargs[k], list) else kwargs[k]) != n_plots}
    fargs['legend'] = fargs.pop('legend', len([k for k in {**kwargs, **largs}.keys() if 'label' in k]) != 0)

    # plural arguments ------------------------------------------------
    args    = line.__init__.__code__.co_varnames                        # Get line function arguments

    ax_arg = lambda arg: arg[-2:] in ['_x', '_y']

    plurals = [arg + 's' if not ax_arg(arg) else arg[:-2] + 's' + arg[-2:] for arg in args]

    plurals = list(set(plurals) & set(kwargs.keys()))                   # Intersection of kwargs keys and plurals
    plurals = {k: kwargs.pop(k) for k in plurals}                       # Dictionary of plurals

    def plural(i):
        """
        Get plural arguments of the ith plot.

        :param i: index
        """

        _args = {}

        for k in plurals.keys():
            _k = k[:-3] + k[-2:] if ax_arg(k) else k[:-1]
            _args[_k] = plurals[k][i]

        return _args

    # curve arguments ------------------------------------------------
    cargs = {k: plurals.pop(k) for k in dc(plurals).keys() if isinstance(plurals[k], list) and (len(plurals[k]) != n_plots or all([isinstance(arg, list) for arg in plurals[k]]))}

    ###############################
    #           FIGURE            #
    ###############################
    N = min(n_plots, ceil(n_plots/rows))
    M = rows

    height = 3.5 if M == 1 else 4

    if fig is None:
        if figsize is None:
            fig = figure((5 * N, height * M), backend=fargs['backend'])
        else:
            fig = figure(figsize)

    ###############################
    #            PLOT             #
    ###############################
    
    shape = (M, N) if shape is None else shape
    
    for n in range(n_plots):
        
        coords = (floor(n/(N)), (n % (N)))

        ax_transient = plt.subplot2grid(shape,
                                        coords,
                                        rowspan=1,
                                        colspan=1)

        # Margins
        plt.subplots_adjust(top=     0.88,
                            bottom=  0.11,
                            left=    0.1                              if left   is not None else left,
                            right=   0.85 if M == 1 else 0.75         if right  is not None else right,
                            wspace=  0.6                              if wspace is not None else wspace,
                            hspace=  0.35                             if hspace is not None else hspace)

        # Retrieve curve arguments
        _cargs = {}
        for k in cargs.keys():
            _curve_arg = cargs[k]
            if isinstance(_curve_arg, list):
                # multiple curves per panel -> plural argument to comparison
                if len(_curve_arg) == n_plots and all([isinstance(_arg, list) for _arg in _curve_arg]):
                    # each panel is passed a different list of curve arguments
                    _cargs[k] = _curve_arg[n]
                else:
                    # the same list of curve arguments is passed to all panels
                    _cargs[k] = _curve_arg
            else:
                # single curve per panel
                _k = k[:-3] + k[-2:] if ax_arg(k) else k[:-1]
                _cargs[_k] = _curve_arg

        # Pass keyword arguments to last
        args = {**kwargs, **plural(n), **_cargs} if n != n_plots - 1 else {**kwargs, **plural(n), **_cargs, **fargs, **largs}

        # If y[n] is a list (multiple curves in each plot)
        if isinstance(y[n], list) and isinstance(x[n], list):
            n_curves = len(y[n])
            X = [x[n][i] for i in range(n_curves)]
            Y = [y[n][i] for i in range(n_curves)]
            F = [f[n][i] for i in range(n_curves)] if isinstance(f, list) and isinstance(f[n], list) else\
                f[n] if isinstance(f, list) else\
                f if f is not None else\
                line
        elif isinstance(y[n], list):
            n_curves = len(y[n])
            X = x[n] if isinstance(x, list) else\
                x
            Y = [y[n][i] for i in range(n_curves)]
            F = [f[n][i] for i in range(n_curves)] if isinstance(f, list) and isinstance(f[n], list) else\
                f[n] if isinstance(f, list) else\
                f if f is not None else\
                line
        elif  isinstance(x[n], list):
            n_curves = len(x[n])
            X = [x[n][i] for i in range(n_curves)]
            Y = y[n] if isinstance(y, list) else\
                y
            F = [f[n][i] for i in range(n_curves)] if isinstance(f, list) and isinstance(f[n], list) else\
                f[n] if isinstance(f, list) else\
                f if f is not None else\
                line
        else:
            X = x[n] if not single_x else x
            Y = y[n] if not single_y else y
            F = f[n] if isinstance(f, list) else\
                f if f is not None else\
                line

        comparison(X,
                   Y,
                   F,
                   ax=ax_transient, fig=fig,
                   
                   legend=args.pop('legend') if n == n_plots-1 else False,         # Avoid conflict
                   
                   **args
                   )

    # Margins
    plt.subplots_adjust(top=     1.00                             if top    is None else top,
                        bottom=  0.11                             if bottom is None else bottom,
                        left=    0.1                              if left   is None else left,
                        right=   (0.85 if M == 1 else 0.75)       if right  is None else right,
                        wspace=  0.6                              if wspace is None else wspace,
                        hspace=  0.35                             if hspace is None else hspace)

    if fargs['legend']:

        # Legend placement
        legend = (c for c in plt.gca().get_children() if isinstance(c, mpl.legend.Legend))

        # Save figure (necessary step for correct legend positioning, thanks to
        # the _bbox_extra_artists_ argument of _plt.savefig_)
        plt.savefig(os.path.join(tmp(), 'tmp.pdf'),
                    bbox_extra_artists=legend,
                    )
    if show:
        plt.show()
