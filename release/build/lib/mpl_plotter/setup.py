import matplotlib as mpl
import matplotlib.pyplot as plt


def figure(figsize=(6, 6), backend='Qt5Agg'):
    mpl.use(backend)
    return plt.figure(figsize=figsize)

