import numpy as np
import matplotlib as mpl

from alexandria.logic import if_none
from alexandria.shell import print_color
from alexandria.data_structs.array import lists_to_ndarrays

from mpl_plotter import figure
from mpl_plotter.two_d import line
from mpl_plotter.utils import input_match
from mpl_plotter.color.schemes import one
from mpl_plotter.two_d.comparison import comparison


def singles(x,
            y,
            f=None,
            labels=None, legend_labels=None,
            show=False, save=False, filename=None, dest=None,
            **kwargs):

    # Input
    x, y = lists_to_ndarrays(x, y)
    x = input_match(x, y)
    # Plotting function
    if isinstance(f, type(None)):
        f = f if np.array([f]).size == len(y) else [line for i in range(len(y))]
    else:
        f = f if np.array([f]).size == len(y) else [line for i in range(len(y))]

    # Defaults
    backend       = kwargs.pop('backend',       'Qt5Agg')                                                     # Setup
    fig           = kwargs.pop('fig',           figure((5*len(y), 3.5), backend=backend))
    legend        = kwargs.pop('legend',        True if not isinstance(legend_labels, type(None)) else True)  # Legend
    legend_loc    = kwargs.pop('legend_loc',    (0.875, 0.55))

    # Import Pyplot after backend choice
    import matplotlib.pyplot as plt

    # Plot
    for i in range(len(y)):
        ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
        if i < (len(y) - 1):
            f[i](x=x[i], y=y[i], color=one()[i], ax=ax_transient, fig=fig,
                 y_label=labels[i] if not isinstance(labels, type(None)) else None,
                 plot_label=legend_labels[i] if not isinstance(legend_labels, type(None)) else None,
                 backend=backend
                 )
        else:
            f[i](x=x[i], y=y[i], color=one()[i], ax=ax_transient, fig=fig,
                 y_label=labels[i] if not isinstance(labels, type(None)) else None,
                 legend=True if not isinstance(legend_labels, type(None)) else False,
                 plot_label=legend_labels[i] if not isinstance(legend_labels, type(None)) else None,
                 legend_loc=legend_loc,
                 backend=backend,
                 **kwargs)

    # Margins
    plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)

    # Save figure (necessary step for correct legend positioning, thanks to
    # the _bbox_extra_artists_ argument of _plt.savefig_)
    if save:
        if not isinstance(filename, type(None)) and not isinstance(dest, type(None)):
            plt.savefig(f"{dest}/{filename}.pdf")
        else:
            filename = input("Filename:") if isinstance(filename, type(None)) \
                else filename
            dest = input("Destination directory:") if isinstance(dest, type(None)) \
                else dest
            try:
                plt.savefig(f"{dest}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
            except FileNotFoundError:
                print_color("Destination directory does not exist. Please enter destination directory again:", "blue")
                dest = input()
                plt.savefig(f"{dest}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
    if show:
        plt.show()


def comparison(x,
               y,
               f=None,
               axis_labels=None, legend_labels=None,
               zorders=None, colors=None, alphas=None,
               show=False, save=False, filename=None, dest=None,
               **kwargs):

    # Input check
    x, y = lists_to_ndarrays(x, y)
    x = input_match(x, y)
    # Plotting function
    if isinstance(f, type(None)):
        f = f if np.array([f]).size == len(y) else [line for i in range(len(y))]
    else:
        f = f if np.array([f]).size == len(y) else [line for i in range(len(y))]

    # Special parameters
    zorders = if_none(zorders, np.arange(len(y) + 1, 0, -1))
    colors  = if_none(colors, [one()[n] for n in range(len(y))])
    alphas  = if_none(alphas, np.ones(len(y)))

    # Regular defaults
    backend    = kwargs.pop('backend', None)                    # Setup
    legend_loc = kwargs.pop('legend_loc', (0.875, 0.55))     # Legend

    # Figure setup
    fig = figure((5 * len(y), 3.5), backend=backend)
    import matplotlib.pyplot as plt

    # Plot
    for i in range(len(y)):
        ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
        if i < (len(y) - 1):
            comparison([x[i][n] for n in range(len(y[1]))],
                       [y[i][n] for n in range(len(y[1]))],
                       f[i],
                       ax=ax_transient, fig=fig, backend=backend,
                       y_label=axis_labels[i] if not isinstance(axis_labels, type(None)) else None,
                       zorders=zorders, colors=colors, alphas=alphas,
                       legend=False
                       )
        else:
            comparison([x[i][n] for n in range(len(y[1]))],
                       [y[i][n] for n in range(len(y[1]))],
                       f[i],
                       ax=ax_transient, fig=fig, backend=backend,
                       y_label=axis_labels[i] if not isinstance(axis_labels, type(None)) else None,
                       zorders=zorders, colors=colors, alphas=alphas,
                       plot_labels=legend_labels,
                       legend=True if not isinstance(legend_labels, type(None)) else False,
                       legend_loc=legend_loc,
                       **kwargs
                       )

    # Margins
    plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)

    # Legend placement
    legend = (c for c in ax_transient.get_children() if isinstance(c, mpl.legend.Legend))

    # Save figure (necessary step for correct legend positioning, thanks to
    # the _bbox_extra_artists_ argument of _plt.savefig_)
    if save:
        filename = input("Filename:") if isinstance(filename, type(None)) \
            else filename
        dest = input("Destination directory:") if isinstance(dest, type(None)) \
            else dest
        try:
            plt.savefig(f"{dest}/{filename}.pdf",
                        bbox_extra_artists=legend,
                        )
        except FileNotFoundError:
            print_color("Destination directory does not exist. Please enter destination directory again:", "blue")
            dest = input()
            plt.savefig(f"{dest}/{filename}.pdf",
                        bbox_extra_artists=legend,
                        )
    if show:
        plt.show()
