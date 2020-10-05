import numpy as np
import pandas as pd
import matplotlib.tri as mtri
from scipy import ndimage


class Data2D:

    def __init__(self):
        pass

    def line(self, f, u0, un, n):
        """
        :param f:
        :param u0:
        :param un:
        :param n:
        :return:
        """
        u = np.linspace(u0, un, n)
        v = f(u)
        return u, v

    def heatmap(self, f, u0, v0, un, vn, n):
        """
        :param f:
        :param u0:
        :param v0:
        :param un:
        :param vn:
        :param n:
        :return: f(u, v) in Pandas DataFrame format
        """
        u = np.linspace(u0, un, n)
        v = np.linspace(v0, vn, n)
        um, vm = np.meshgrid(u, v)
        w = f(um, vm)
        w = pd.DataFrame(w, index=u, columns=v)
        return w

    # def volumetric_slice(self, f, u0, v0, un, vn, w_slice, n):
    #     """
    #     :param f:
    #     :param u0:
    #     :param v0:
    #     :param un:
    #     :param vn:
    #     :param w_slice:
    #     :param n:
    #     :return:
    #     """
    #     u = np.linspace(u0, un, n)
    #     v = np.linspace(v0, vn, n)
    #     u, v = np.meshgrid(u, v)
    #     c = f(u, v, w_slice)
    #     return u, v, c


class Data3D:
    def __init__(self):
        pass

    def line(self, f, g, u0, un, n):
        """
        :param f:
        :param g:
        :param u0:
        :param un:
        :param n:
        :return:
        """
        u = np.linspace(u0, un, n)
        v = f(u)
        w = g(u)
        return u, v, w

    def surface(self, f, u0, un, v0, vn, n):
        """
        :param f:
        :param u0:
        :param un:
        :param v0:
        :param vn:
        :param n:
        :return:
        """
        u = np.linspace(u0, un, n)
        v = np.linspace(v0, vn, n)
        u, v = np.meshgrid(u, v)
        w = f(u, v)
        return u, v, w

    def volumetric(self, f, u0, un, v0, vn, w0, wn, n):
        """
        :param f:
        :param u0:
        :param un:
        :param v0:
        :param vn:
        :param w0:
        :param wn:
        :param n:
        :return:
        """
        u, v, w = np.mgrid[u0:un, v0:vn, w0:wn]
        vol = np.zeros((1, 1, 1))
        pts = f(u, v, w)
        vol[tuple(indices for indices in pts)] = 1
        vol = ndimage.gaussian_filter(vol, 4)
        vol /= vol.max()
        return u.flatten(), v.flatten(), w.flatten(), vol.flatten()

    def triangular_mesh(self, u0, un, v0, vn, f, g, h, n):
        u = np.linspace(u0, un, endpoint=True, num=n)
        v = np.linspace(v0, vn, endpoint=True, num=n)
        u, v = np.meshgrid(u, v)
        u, v = u.flatten(), v.flatten()
        x = f(u, v)
        y = g(u, v)
        z = h(u, v)
        tri = mtri.Triangulation(u, v)
        return x, y, z, tri

