import os
import re
import sys
import datetime as dt
import pandas as pd
from itertools import chain

import matplotlib as mpl
import matplotlib.pyplot as plt
from two_d import line, scatter


def root():
    return os.path.dirname(sys.modules['__main__'].__file__)


def file():
    r = re.compile('.*csv?')
    f = list((filter(r.match, list(chain.from_iterable(chain.from_iterable(os.walk(root())))))))[0]
    return os.path.join(str(root()), f)


def df():
    return pd.read_csv(file())


def nl(df):
    return df.loc[df[" Country_code"] == "NL"]


def to_datetime(dates):
    return [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]


def from_datetime(dt_objs, format='%Y-%m-%d'):
    return [dt.datetime.strftime(d, format) for d in dt_objs]


def pad(r, percent):
    return (r[-1]-r[0])*percent/100


def label(metric):
    return f'{metric.replace(" ", "").replace("_", " ").title()}'


def plot(df, metric):
    x = to_datetime(df["Date_reported"])
    y = df[metric]
    line(x=x, y=y,
         title=label(metric) + ' versus Time: Netherlands', color='darkred', line_width=3,
         more_subplots_left=True, zorder=1,)
    scatter(x=x, y=y,
            title=label(metric) + ' versus Time: Netherlands', c=y, cmap='RdYlBu_r',
            x_label=None,
            y_label=label(metric), y_label_rotation=90,
            x_tick_rotation=60, x_tick_number=5,
            y_tick_number=5, custom_y_tick_labels=[0, 100000],
            date_tick_labels_x=True, date_format='%Y, %b %d',
            zorder=2, filename='demo.png', dpi=150)
    return x, y


x, y = plot(nl(df()), " Cumulative_cases")
