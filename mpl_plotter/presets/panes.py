import numpy as np
import matplotlib as mpl

from mpl_plotter.setup import figure
from mpl_plotter.color.schemes import one
from mpl_plotter.presets.custom import two_d

from Alexandria.general.logic import if_none
from Alexandria.constructs.array import lists_to_ndarrays
from Alexandria.general.console import print_color
from Alexandria.constructs.array import internal_array_shape


class Lines:

    def __init__(self, preset=None):
        global line

        if isinstance(preset, type(None)):
            from mpl_plotter.presets.standard.publication import preset2
            line = two_d(direct_preset=preset2).line
        else:
            line = two_d(direct_preset=preset).line

    """
    Pane plots
    """
    @classmethod
    def n_pane_single(cls, x, y,
                      labels=None, legend_labels=None,
                      filename=None, where_does_this_go=None,
                      **kwargs):

        # Regular defaults
        backend = kwargs.pop('backend', None)                   # Setup
        legend_loc = kwargs.pop('legend_loc', (0.875, 0.55))    # Legend
        show = kwargs.pop('show', False)                        # Display
        save = kwargs.pop('save', False)
        legend = kwargs.pop('legend', True if not isinstance(legend_labels, type(None)) else True)  # Legend

        # Figure setup
        fig = figure((5*len(y), 3.5), backend=backend)
        import matplotlib.pyplot as plt

        # Plot
        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            if i < (len(y) - 1):
                line(x=x, y=y[i], color=one()[i], ax=ax_transient, fig=fig,
                     y_label=labels[i] if not isinstance(labels, type(None)) else None,
                     plot_label=legend_labels[i] if not isinstance(legend_labels, type(None)) else None,
                     backend=backend)
            else:
                line(x=x, y=y[i], color=one()[i], ax=ax_transient, fig=fig,
                     y_label=labels[i] if not isinstance(labels, type(None)) else None,
                     legend=True if not isinstance(legend_labels, type(None)) else False,
                     plot_label=legend_labels[i] if not isinstance(legend_labels, type(None)) else None,
                     legend_loc=legend_loc,
                     backend=backend,
                     **kwargs)

        plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)

        if not isinstance(filename, type(None)) and not isinstance(where_does_this_go, type(None)):
            plt.savefig(f"{where_does_this_go}/{filename}.pdf")
            plt.show()
        if show:
            plt.show()

        if save:
            filename = input("Filename:") if isinstance(filename, type(None)) \
                else filename
            where_does_this_go = input("Destination directory:") if isinstance(where_does_this_go, type(None)) \
                else where_does_this_go
            try:
                plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
            except FileNotFoundError:
                print_color("Destination directory does not exist. Destination directory:", "blue")
                where_does_this_go = input()
                plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
        if show:
            plt.show()

    @classmethod
    def n_pane_comparison(cls, t, y,
                          axis_labels=None, legend_labels=None,
                          zorders=None, colors=None, alphas=None,
                          filename=None, where_does_this_go=None,
                          **kwargs):

        # Input check
        t, y = lists_to_ndarrays(t, y)
        t = cls.comparison_input_match(t, y)

        # Special parameters
        zorders = if_none(zorders, np.arange(len(y) + 1, 0, -1))
        colors = if_none(colors, [one()[n] for n in range(len(y))])
        alphas = if_none(alphas, np.ones(len(y)))

        # Regular defaults
        backend = kwargs.pop('backend', None)                    # Setup
        legend_loc = kwargs.pop('legend_loc', (0.875, 0.55))     # Legend
        show = kwargs.pop('show', False)                         # Display
        save = kwargs.pop('save', False)

        # Figure setup
        fig = figure((5 * len(y), 3.5), backend=backend)
        import matplotlib.pyplot as plt

        # Plot
        for i in range(len(y)):
            ax_transient = plt.subplot2grid((1, len(y)), (0, i), rowspan=1, colspan=1)
            if i < (len(y) - 1):
                cls.comparison([t[i][n] for n in range(len(y[1]))], [y[i][n] for n in range(len(y[1]))],
                               ax=ax_transient, fig=fig, backend=backend,
                               y_label=axis_labels[i] if not isinstance(axis_labels, type(None)) else None,
                               zorders=zorders, colors=colors, alphas=alphas,
                               legend=False
                               )
            else:
                cls.comparison([t[i][n] for n in range(len(y[1]))], [y[i][n] for n in range(len(y[1]))],
                               ax=ax_transient, fig=fig, backend=backend,
                               y_label=axis_labels[i] if not isinstance(axis_labels, type(None)) else None,
                               zorders=zorders, colors=colors, alphas=alphas,
                               plot_labels=legend_labels,
                               legend=True if not isinstance(legend_labels, type(None)) else False,
                               legend_loc=legend_loc,
                               **kwargs
                               )

        plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)
        legend = (c for c in ax_transient.get_children() if isinstance(c, mpl.legend.Legend))

        if save:
            filename = input("Filename:") if isinstance(filename, type(None)) \
                else filename
            where_does_this_go = input("Destination directory:") if isinstance(where_does_this_go, type(None)) \
                else where_does_this_go
            try:
                plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
            except FileNotFoundError:
                print_color("Destination directory does not exist. Destination directory:", "blue")
                where_does_this_go = input()
                plt.savefig(f"{where_does_this_go}/{filename}.pdf",
                            bbox_extra_artists=legend,
                            )
        if show:
            plt.show()

    """
    Single line plots
    """

    @classmethod
    def comparison(cls, x, y,
                   zorders=None, colors=None, plot_labels=None, alphas=None,
                   **kwargs):

        # Regular defaults
        backend = kwargs.pop('backend', "Qt5Agg")           # Setup
        fig = kwargs.pop('fig', None)
        ax = kwargs.pop('ax', None)
        demo_pad_plot = kwargs.pop('demo_pad_plot', False)  # Axes
        y_label = kwargs.pop('y_label', None)               # Labels
        legend = kwargs.pop('legend', True if not isinstance(plot_labels, type(None)) else True)  # Legend
        legend_loc = kwargs.pop('legend_loc', (0.7, 0.2))

        # Color scheme
        colorscheme = colors if not isinstance(colors, type(None)) else one()

        # Aspect ratio calculation
        y_max = max(y[n].max() for n in range(len(y)))
        y_min = min(y[n].min() for n in range(len(y)))
        span_y = abs(y_max-y_min)

        x_max = max(x[n].max() for n in range(len(x)))
        x_min = min(x[n].min() for n in range(len(x)))
        span_x = abs(x_max-x_min)

        for i in range(len(y)):
            if i < (len(y) - 1):
                line(x=x[i], y=y[i], color=colorscheme[i], ax=ax, fig=fig,
                     zorder=zorders[i] if not isinstance(zorders, type(None)) else None,
                     alpha=alphas[i] if not isinstance(alphas, type(None)) else None,
                     plot_label=plot_labels[i] if not isinstance(plot_labels, type(None)) else None,
                     resize_axes=False, grid=False,
                     backend=backend,
                     )
            else:
                line(x=x[i], y=y[i], color=colorscheme[i], ax=ax, fig=fig,
                     zorder=zorders[i] if not isinstance(zorders, type(None)) else None,
                     alpha=alphas[i] if not isinstance(alphas, type(None)) else None,
                     plot_label=plot_labels[i] if not isinstance(plot_labels, type(None)) else None,
                     y_label=y_label,
                     legend=legend, legend_loc=legend_loc,
                     x_bounds=[x_min - 0.05 * span_x,
                               x_max + 0.05 * span_x],
                     y_bounds=[y_min - 0.05 * span_y,
                               y_max + 0.05 * span_y],
                     demo_pad_plot=demo_pad_plot,
                     y_custom_tick_locations=[y_min,
                                              y_max],
                     x_custom_tick_locations=[x_min,
                                              x_max],
                     backend=backend,
                     **kwargs
                     )

    @classmethod
    def comparison_input_match(cls, x, y):
        if not (internal_array_shape(y) == internal_array_shape(y)[0]).all():
            raise ValueError(f"Arrays in _y_ have different shapes:\n{*internal_array_shape(y),}")
        if x.shape != y.shape:
            if x.ndim == 1:
                t = np.array(list([x for n in range(y.shape[1])] for i in range(y.shape[0]))).squeeze()
                return t
            else:
                raise ValueError("_t_ and _y_ mismatch")
