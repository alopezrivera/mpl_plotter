from mpl_plotter.two_d import line as mpl_line


def line(x, y, demo_pad_plot=True,
         **kwargs):
    mpl_line(x=x, y=y,
             demo_pad_plot=demo_pad_plot,
             x_tick_number=3, tick_label_size_x=15,
             y_tick_number=3, tick_label_size_y=15,
             y_label_size=20, x_label_size=20,
             tick_ndecimals_y=3,
             **kwargs
             )
