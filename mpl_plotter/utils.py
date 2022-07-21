import os

from sys import platform
from pathlib import Path

import numpy as np


def tmp():
    """
    Return the machine's temporary file directory.
    """
    
    tmp = os.path.join('/tmp/' if platform != 'win32' else os.environ['TEMP'], '.mpl_plotter')
    
    Path(tmp).mkdir(parents=True, exist_ok=True)
    
    return tmp


def ensure_ndarray(a):
    """
    Return _a_ if it is a NumPy array, or else return _a_
    as a NumPy array.
    """
    return np.asarray(a) if not isinstance(a, np.ndarray) else a


def span(a):
    """
    Find the difference between the highest and lowest elements
    of a list or array.

    :param a: Array.

    :type a: np.ndarray | list

    :return: [float] Array span.
    """
    a = ensure_ndarray(a)
    if a.size > 1:
        a_s = a + a.min() if a.min() < 0 else a
        return a_s.max() - a_s.min()
    elif a.size == 1:
        return 0


def bounds(d, u, l, up, lp, v):
        # Upper and lower bounds
        if isinstance(u, type(None)):
            u = d.max()
        else:
            up = 0
        if isinstance(l, type(None)):
            l = d.min()
        else:
            lp = 0
        # Bounds vector
        if isinstance(v, type(None)):
            v = [l, u]
        if isinstance(v[0], type(None)):
            v[0] = l
        if isinstance(v[1], type(None)):
            v[1] = u
        return v, up, lp
