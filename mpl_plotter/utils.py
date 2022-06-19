import numpy as np


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