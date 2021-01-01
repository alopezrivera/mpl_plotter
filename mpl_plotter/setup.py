import matplotlib as mpl


def figure(figsize=(6, 6), backend='Qt5Agg'):
    mpl.use(backend)
    import matplotlib.pyplot as plt
    return plt.figure(figsize=figsize)

