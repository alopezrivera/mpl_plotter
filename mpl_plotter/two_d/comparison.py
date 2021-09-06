import numpy as np
import matplotlib as mpl

from alexandria.paths import home
from alexandria.data_structs.array import lists_to_ndarrays

from mpl_plotter import figure
from mpl_plotter.two_d import line
from mpl_plotter.utils import input_match
from mpl_plotter.color.schemes import colorscheme_one


def comparison(x,
               y,
               f=None,
               plot_labels=None,
               zorders=None, colors=None, alphas=None,
               **kwargs):
    """
    Plot _n_ arrays of values over _n_ domains.
    The limits of the plot will be adjusted to the upper and lower limits
    of all _x_ and _y_.

    :param x:               Domains.
    :param y:               Values.
    :param f:               Functions used to plot y(x)
    :param plot_labels:     Plot labels
    :param zorders:         Determine plot layout
    :param colors:          Determine color of each plot
    :param alphas:          Determine alpha of each plot
    :param kwargs:          MPL Plotter plotting class keyword arguments for
                            further customization

    :type x:                list of list or list of np.ndarray
    :type y:                list of list or list of np.ndarray
    :type f:                list of plot
    :type zorders:          list of float
    :type colors:           list of str
    :type plot_labels:      list of str
    :type alphas:           list of float
    """
    # Input
    x, y = lists_to_ndarrays(x, y)
    if y.ndim == 1:
        if all([not isinstance(v, np.ndarray) for v in y]):
            # Single curve
            y = np.array([y])
            x = input_match(x, y)
            # Plotting function
            if isinstance(f, type(None)):
                f = np.array([line])
            else:
                f = np.array([f])
        else:
            # Curves of different sizes
            mask_x = np.array([a.size != 0 for a in x])
            mask_y = np.array([a.size != 0 for a in y])

            mask = mask_x * mask_y  # Ensure that any x-y array pairs with an empty array are removed

            x = x[mask]
            y = y[mask]
            f = np.array(f)[mask]

    elif y.ndim >= 2:
        # _n_ curves
        x = input_match(x, y)
        # Plotting function
        if isinstance(f, type(None)):
            f = f if np.array([f]).size == len(y) else [line for i in range(len(y))]
        else:
            f = f if np.array([f]).size == len(y) else [f for i in range(len(y))]

    # Defaults
    backend = kwargs.pop('backend', "Qt5Agg")  # Setup
    fig = kwargs.pop('fig', None)
    ax = kwargs.pop('ax', None)
    demo_pad_plot = kwargs.pop('demo_pad_plot', False)  # Axes
    x_label = kwargs.pop('x_label', None)  # Labels
    y_label = kwargs.pop('y_label', None)
    legend = kwargs.pop('legend', True if not isinstance(plot_labels, type(None)) else False)  # Legend
    legend_loc = kwargs.pop('legend_loc', (0.7, 0.2))
    show = kwargs.pop('show', False)

    # Color scheme
    colors = colors if not isinstance(colors, type(None)) else colorscheme_one()

    # Limits
    y_max = max(y[n].max() for n in range(len(y)))
    y_min = min(y[n].min() for n in range(len(y)))
    span_y = abs(y_max - y_min)

    x_max = max(x[n].max() for n in range(len(x)))
    x_min = min(x[n].min() for n in range(len(x)))
    span_x = abs(x_max - x_min)

    for i in range(len(y)):
        if i < (len(y) - 1):
            f[i](x=x[i], y=y[i],  # Main

                 color=colors[i],  # Customization
                 zorder=zorders[i] if not isinstance(zorders, type(None)) else None,
                 alpha=alphas[i] if not isinstance(alphas, type(None)) else None,
                 plot_label=plot_labels[i] if not isinstance(plot_labels, type(None)) else None,

                 ax=ax, fig=fig, backend=backend,  # **kwargs

                 resize_axes=False, grid=False,  # Default
                 )
        else:
            f[i](x=x[i], y=y[i],  # Main

                 color=colors[i],  # Customization
                 zorder=zorders[i] if not isinstance(zorders, type(None)) else None,
                 alpha=alphas[i] if not isinstance(alphas, type(None)) else None,
                 plot_label=plot_labels[i] if not isinstance(plot_labels, type(None)) else None,
                 x_label=x_label,
                 y_label=y_label,

                 legend=legend, legend_loc=legend_loc,  # Automatic
                 demo_pad_plot=demo_pad_plot,
                 x_bounds=[x_min - 0.05 * span_x,
                           x_max + 0.05 * span_x],
                 y_bounds=[y_min - 0.05 * span_y,
                           y_max + 0.05 * span_y],
                 y_custom_tick_locations=[y_min,
                                          y_max],
                 x_custom_tick_locations=[x_min,
                                          x_max],

                 ax=ax, fig=fig, backend=backend,  # **kwargs
                 **kwargs
                 )

    # Margins
    import matplotlib.pyplot as plt
    plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)

    # Legend placement
    legend = (c for c in plt.gca().get_children() if isinstance(c, mpl.legend.Legend))

    # Save figure (necessary step for correct legend positioning, thanks to
    # the _bbox_extra_artists_ argument of _plt.savefig_)
    plt.savefig(f"{home()}/temp.pdf",
                bbox_extra_artists=legend,
                )
    if show:
        plt.show()
