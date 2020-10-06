import os
import re
import sys
import pandas as pd
import datetime as dt
from itertools import chain

from scipy.interpolate import UnivariateSpline

"""
mpl_plotter
    MatPlotLib-based plotting library developed by Antonio Lopez Rivera
"""
from mpl_plotter.two_d import line, scatter
"""
    https://test.pypi.org/project/mpl-plotter/
"""


def root():
    return os.path.dirname(sys.modules['__main__'].__file__)


def file(folder="data"):
    regx = re.compile('.*csv?')
    path = os.path.join(root(), folder)
    file = list((filter(regx.match,
                        list(chain.from_iterable(chain.from_iterable(os.walk(path)))))))[0]
    return os.path.join(path, file)


def df():
    return pd.read_csv("file.csv")


def country(df, code):
    return df.loc[df[" Country_code"] == f"{code}"]


def to_datetime(dates):
    return [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]


def from_datetime(dt_objs, format='%Y-%m-%d'):
    return [dt.datetime.strftime(d, format) for d in dt_objs]


def to_float(dates, patient_zero_yy_minusdays=(2020, 20)):
    _d = []
    for date in dates:
        d = str(date).split('-')
        d = (float(d[0])-patient_zero_yy_minusdays[0])*365 - patient_zero_yy_minusdays[1] + (float(d[1]))*30 + float(d[2])
        _d.append(d)
    return _d


def pad(r, percent):
    return (r[-1]-r[0])*percent/100


def label(metric):
    return f'{metric.replace(" ", "").replace("_", " ").title()}'


def derivative(x, y):
    _x = to_float(x)[0::7]
    _y = y[0::7]
    return UnivariateSpline(_x, _y).derivative()(to_float(x))


class CasesVTime:
    def __init__(self, df, metric=" Cumulative_cases"):
        self.x = to_datetime(df["Date_reported"])
        self.y = df[metric]
        self.dy = derivative(self.x, self.y)
        self.metric = metric
        # Bounds
        self.x_bounds = [0, 260]
        self.y_bounds = [0, 75000]
        self.custom_y_ticklabels = [0, 75]
        self.hard_bounds = True
        # Color
        self.color = self.dy
        self.cb_vmin = 0
        self.cb_vmax = 1300
        # Labels
        self.title = label(self.metric) + ' versus Time: Netherlands'
        self.title_y = 1.025
        self.cb_title = '$\Delta$: 1 day'
        self.y_label = '$x 1000$'
        self.y_label_rotation = 90
        self.y_label_pad = 10
        self.y_label_size = 10
        self.tick_ndecimals = 0
        # Filename
        self.filename = 'CasesVTime'

    def derivative(self, second_derivative=False):
        self.y = self.dy
        # Bounds
        self.x_bounds = [0, 260]
        self.y_bounds = [0, 1300]
        self.custom_y_ticklabels = None
        # Labels
        self.title = r'$\frac{\delta}{\delta t}$(' + label(self.metric) + ') versus Time: Netherlands'
        self.title_y = 1.05
        self.y_label = ''
        self.y_label_rotation = None
        self.y_label_pad = None
        self.y_label_size = None
        # Color
        self.cb_vmin = self.y_bounds[0]
        self.cb_vmax = self.y_bounds[1]
        # Filename
        self.filename = 'dCasesVTime'
        if second_derivative is True:
            # Color
            self.color = derivative(self.x, self.dy)
            self.cb_vmin = self.color.min()
            self.cb_vmax = self.color.max()
            # Labels
            self.cb_title = r'$\frac{\delta^2}{\delta t^2}($' + label(self.metric) + '): 1 day'
            # Filename
            self.filename = 'd2CasesVTime'
        return self

    def line(self):
        line(x=to_float(self.x), y=self.y, norm=self.color, line_width=3, backend='Qt5Agg',
             # Color params
             cmap='copper_r',
             # Figure params
             figsize=(6, 8), more_subplots_left=True, zorder=1,
             )
        scatter(x=to_float(self.x), y=self.y,
                x_bounds=self.x_bounds,
                y_bounds=self.y_bounds,
                # Point parameters
                point_size=10,
                marker='_',
                # Labels
                x_label='Days since patient 0', x_label_pad=15, x_label_size=15, x_tick_rotation=60, x_tick_number=5,
                y_label=self.y_label, y_label_rotation=self.y_label_rotation,
                y_label_pad=self.y_label_pad, y_label_size=self.y_label_size,
                custom_y_tick_labels=self.custom_y_ticklabels, y_tick_number=5,
                tick_ndecimals=self.tick_ndecimals,
                # Color params
                c=self.color, cmap='copper', background_color_plot='#f5f5f5',
                color_bar=True, cb_vmin=self.cb_vmin, cb_vmax=self.cb_vmax, cb_tick_number=6,
                cb_title=self.cb_title, cb_orientation='horizontal', cb_pad=0.175, shrink=1, cb_title_size=16,
                cb_hard_bounds=self.hard_bounds,
                # Title and figure params
                title=self.title, title_size=16, title_y=self.title_y,
                font='Consolas', subplot=True, more_subplots_left=True, zorder=2,
                # Discarded
                # date_tick_labels_x=True, date_format='%b %d',
                # background_color_figure='#ffca43',
                )
        return self

    def save(self):
        import matplotlib.pyplot as plt
        plt.savefig('results/' + self.filename + '_final.pdf')
        return self

    def show(self):
        import matplotlib.pyplot as plt
        plt.tight_layout()
        plt.show()

    def cnvs(self):
        import matplotlib.pyplot as plt
        return plt.gcf().canvas


CasesVTime(country(df(), 'NL')).line().show()  # derivative(second_derivative=False)
