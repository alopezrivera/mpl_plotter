# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
MPL Plotter utilities
---------------------
"""


import numpy as np
from alexandria.data_structs.array import internal_array_shape


def input_match(x, y):
    """
    Check whether the shapes of the arrays contained inside the domains array _x_
    and the images array _y_ are equal.

    :param x: Domains array
    :param y: Images array

    :return: a domains array so as to match the shapes of the arrays contained in _y_
    - If the shape of _x_ and _y_ does NOT match:
        - If the dimension of _x_ is 1:
            - If the internal array shapes inside _y_ do NOT match:
                - Raise ValueError
            - Else:
                - return an array of length y.shape[0] containing _x_ in each element
        - Else:
            - Raise ValueError
    - Else:
        - If the internal array shapes of _x_ and _y_ do NOT match:
            - Raise ValueError
        - Else:
            - Return _x_ unmodified
    """
    if x.shape != y.shape:
        if x.ndim == 1:
            if y.ndim == 2:
                # If _y_ is an array which contains vectors (two-dimensional)
                if not (internal_array_shape(y) == internal_array_shape(y)[0]).all() \
                        or not (internal_array_shape(y) == x.shape).all():
                    # If the shapes of the internal arrays of _y_ differ between each other or
                    # from the shape of _x_:
                    raise ValueError(f"_x_ is a one-dimensional array, but the internal arrays in "
                                     f"_y_ have different shapes:\n{*internal_array_shape(y),}")
                else:
                    # Return a domains array of length y.shape[0] containing the one-dimensional
                    # array _x_ (the domain of all images) in each element.
                    _x = np.array([x for n in range(y.shape[0])]).squeeze()
                    return _x
            if y.ndim == 3:
                # If _y_ is an array which contains arrays of vectors (three-dimensional)
                if not (internal_array_shape(y) == internal_array_shape(y)[0]).all() \
                        or not all([(internal_array_shape(y[n]) == x.shape).all() for n in range(len(y))]):
                    raise ValueError(f"_x_ is a one-dimensional array, but the internal arrays in "
                                     f"_y_ have different shapes:\n{*internal_array_shape(y),}")
                _x = np.array([[x for n in range(y.shape[1])] for i in range(y.shape[0])]).squeeze()
                return _x
        else:
            # _x_ is not one-dimensional and the shapes of the internal arrays of _x_ and _y_ do not match
            raise ValueError("The internal dimensions of the input arrays to MPL Plotter input_match do not match.")
    else:
        if not np.array_equal(internal_array_shape(y), internal_array_shape(x)):
            # The shape of _x_ and _y_ matches, but the shapes of their internal arrays do not
            raise ValueError(f"The dimensions of the arrays contained in _x_ and _y_ do not match.")
        else:
            # The shapes of _x_ and _y_ match, as well as those of their internal arrays
            return x
