u, v = np.mgrid[q1_min:q1_max:n, q2_min:q2_max:n]
u, v = u.flatten(), v.flatten()

x = np.sin(v) * np.cos(u)
y = np.sin(u)
z = np.cos(u) * np.cos(v)

cmap = mapstack(['Blues_r', 'Oranges'])

import matplotlib.tri as mtri
import matplotlib.pyplot as plt

tri = mtri.Triangulation(u, v)

fig = figure()
ax = fig.add_subplot(projection='3d')
norm = x
graph = ax.plot_trisurf(x, y, z,
                        triangles=tri.triangles,
                        alpha=1,
                        # norm=Normalize(vmin=norm.min(), vmax=norm.max()),
                        # cmap=plt.cm.Blues
                        )


def map_colors(p3dc, func,
               cmap='viridis',
               vmin=None, vmax=None):
    """
    Color a tri-mesh according to a function evaluated in each barycentre.

    p3dc: a Poly3DCollection, as returned e.g. by ax.plot_trisurf
    func: a single-valued function of 3 arrays: x, y, z
    cmap: a colormap NAME, as a string

    Returns a ScalarMappable that can be used to instantiate a colorbar.
    """

    from matplotlib.cm import ScalarMappable, get_cmap
    from matplotlib.colors import Normalize
    from numpy import array

    # reconstruct the triangles from internal data
    x, y, z, _ = p3dc._vec
    slices = p3dc._segslices
    triangles = array([array((x[s], y[s], z[s])).T for s in slices])

    # compute the barycentres for each triangle
    xb, yb, zb = triangles.mean(axis=1).T

    # compute the function in the barycentres
    values = func(xb, yb, zb)

    # usual stuff
    norm = Normalize(vmin=vmin, vmax=vmax)
    colors = get_cmap(cmap)(norm(values))

    # set the face colors of the Poly3DCollection
    p3dc.set_fc(colors)

    # if the caller wants a colorbar, they need this
    return ScalarMappable(cmap=cmap, norm=norm)


m = map_colors(graph, lambda x, y, z: np.array([np.linalg.norm(coords) for coords in g(x, y, z).T]),
               cmap=cmap)

plt.colorbar(m, shrink=0.67, aspect=16.7)

plt.show()