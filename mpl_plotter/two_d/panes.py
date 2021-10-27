# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Pane plot method
----------------
"""


import numpy as np
from math import floor, ceil
import matplotlib as mpl
import matplotlib.pyplot as plt

from alexandria.paths import home

from mpl_plotter import figure
from mpl_plotter.two_d import line
from mpl_plotter.two_d.comparison import comparison


def panes(x,
          y,
          f=None,
          fig=None,
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
    Panes
    -----

    # Inputs
    The panes function supports numerical inputs in the following forms:
    |   x                      |   y                       |  result  |  notes                                          |
    |  ---                     |  ---                      |  ---     |  ---                                            |
    |  array                   |  array                    |  11      |                                                 |
    |  array                   |  [array, array]           |  12      |  Both `y`s share `x`                            |
    |  [n*[array]              |  [n*[array]]              |  1n      |  Each `y` has an `x`                            |
    |  array                   |  [array, array]           |  21      |  Both `y`s share `x`                            |
    |  [array, array]          |  [array, array]           |  21      |  Each `y` has an `x`                            |
    |  array                   |  [n*[array], n*[array]]   |  2n      |  All curves in all (2) panes share a single `x` |
    |  [array, array]          |  [n*[array], n*[array]]   |  2n      |  All curves in each pane share an `x`           |
    |  [n*[array], n*[array]]  |  [n*[array], n*[array]]   |  2n      |  All curves in all (2) panes have their own `x` |
    |  [m*[n*[array]], m*[n*[array]]]  |  [m*[n*[array]], m*[n*[array]]]   |  mn      |  All curves in all panes have their own `x` |

    where

    * array:  List or NumPy array with numerical values
    * [...]:  List containing ...
    * result: <panes><curves per pane>

    # Arguments
    Arguments are internally classified as FIGURE arguments, PLURAL arguments
    and CURVE arguments, namely:

    * Figure arguments
        Select few arguments which may be input only once in the plotting process, so as
        to avoid conflicts. Ieg: passing `grid=True` twice (`plt.grid(...)`) will result
        in no grid being drawn.
        These are removed from the keyword arguments and used in the last `comparison` call.

    * Special arguments
        Select few arguments (ieg: `plot_labels`), which satisfy the condition of being
            `lists with a length different to that of y`
        and which, for aesthetic purposes, must be applied only once.

        In the case of `plot_labels`, if `plot_labels` is a list of length different to that
        of `y`, it is assumed that
            - The nth curve of each pane shares a label with the nth curve of all other panes
        and so a legend displaying the labels of the last pane will be displayed.

    * Plural arguments
        Arguments with a keyword equal to any of the arguments which can be passed to the
          `line`
        2D plotter, in plural tense. The line plotter is chosen as it shares all general
        arguments with the other 2D plotter functions.
        The plural arguments are assumed to be
          `lists of length equal to the number of panes`
        and thus modify each pane. Ieg: x_tick_labels=[1, 2, 3] will set the tick labels
        of the x axes to 1, 2 and 3 respectively in a 3-pane plot.

    * Curve arguments
        Curve arguments are passed as plurals to the comparison function, as they are
          `lists with a length different to that of y`
        (thus they can't apply to each pane) and they are assumed to have a length equal
        to the number of curves in each plot.


    :type x:                list of list or list of np.ndarray or np.ndarray
    :type y:                list of list or list of np.ndarray or np.ndarray
    :type f:                list of function or list of plot
    :type show:             bool
    :type kwargs:           any
    """

    # Input check
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

    # Plot number
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

    # Figure arguments
    fig_par = [                                                         # Get figure specific parameters
                'backend',
                'show',
                'legend',
                'legend_loc'
              ]
    fparams = list(set(fig_par) & set(list(kwargs.keys())))             # Intersection of kwarg keys and fig params
    fparams = {k: kwargs.pop(k) for k in fparams}                       # Dictionary of figure parameters

    # Plurals
    params  = line.__init__.__code__.co_varnames                        # Get line function parameters
    plurals = [param + 's' for param in params]                         # Parameters: in plural
    plurals = list(set(plurals) & set(list(kwargs.keys())))             # Intersection of kwargs keys and plurals
    plurals = {k: kwargs.pop(k) for k in plurals}                       # Dictionary of plurals

    def plural(i):
        """
        Get plurals parameters of the ith plot.

        :param i: index
        """
        return {k[:-1]: plurals[k][i] for k in list(plurals.keys())}

    # Special
    sparaml = [                                                         # Get special parameters
                'plot_label',
                'plot_labels'
              ]
    sparams = {k: v for k, v in kwargs.items() if k in sparaml and len([v] if not isinstance(v, list) else v) != n_plots}
    sparams = {k: kwargs.pop(k) for k in sparams}                       # Dictionary of figure parameters

    # Curve arguments
    cparams = {k: v for k, v in plurals.items() if isinstance(v, list) and len(v) != n_plots}
    for k in cparams.keys():
        if k in plurals.keys():
            plurals.pop(k)

    # Plot defaults
    fparams['backend']    = fparams.pop('backend',    'Qt5Agg')
    fparams['legend']     = fparams.pop('legend',     len(set([p for p in sparaml if 'label' in p])
                                                          &
                                                          set(list({**sparams, **plurals}.keys())))
                                                      != 0)
    fparams['legend_loc'] = fparams.pop('legend_loc', (0.875, 0.55))

    # Figure setup
    N = min(n_plots, ceil(n_plots/rows))
    M = rows

    height = 3.5 if M == 1 else 4

    if fig is None:
        fig = figure((5 * N, height * M), backend=fparams['backend'])

    # Plot
    for n in range(n_plots):

        ax_transient = plt.subplot2grid((M, N),
                                        (n % rows, floor(n/rows)),
                                        rowspan=1,
                                        colspan=1)

        # Margins
        plt.subplots_adjust(top = 0.88,
                            bottom = 0.11,
                            left=0.1                                if left   is not None else left,
                            right=0.85 if M == 1 else 0.75          if right  is not None else right,
                            wspace=0.6                              if wspace is not None else wspace,
                            hspace=0.35                             if hspace is not None else hspace)

        # Pass keyword arguments to last
        args = {**kwargs, **plural(n), **cparams} if n != n_plots - 1 else {**kwargs, **plural(n), **cparams, **fparams, **sparams}

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

    if fparams['legend']:

        # Legend placement
        legend = (c for c in plt.gca().get_children() if isinstance(c, mpl.legend.Legend))

        # Save figure (necessary step for correct legend positioning, thanks to
        # the _bbox_extra_artists_ argument of _plt.savefig_)
        plt.savefig(f"{home()}/temp.pdf",
                    bbox_extra_artists=legend,
                    )
    if show:
        plt.show()
