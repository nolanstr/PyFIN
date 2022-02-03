import numpy as np


def plot(
    coords,
    connect,
    color="g",
    label="Undeformed",
    overlay_coords=None,
    overlay_color="b",
    overlay_label="Deformed",
    filename=None,
    co=False,
):
    """Display the nodal coordinates and element connectivity
    Parameters
    ----------
    coords : ndarray
        coords[i, j] is the jth coordinate of node i
    connect : ndarray
        connect[i, j] is the jth node of element i
    color : str
        Plot color
    overlay_coords : ndarray
        Truss coords to overlay
    overlay_color : str, optional [b]
        Overlay color
    filename : str
        If given, the name of a file to save the plot to

    Notes
    -----
    if filename is None, the plot will be shown and will clog
    the shell until closed.  Any advice on how to get the plot to not
    clog the shell is much appreciated!
    """
    import matplotlib.pyplot as plt

    if overlay_coords is not None:
        if overlay_coords.shape != coords.shape:
            raise ValueError("coords and overlay_coords must have same shape")

    def margin(points, alt=None):
        """Set a margin to be 2% of largest value"""
        m = 0.02 * np.max(np.abs(points))
        if alt is None:
            return m
        return max(0.02 * np.max(np.abs(alt)), m)

    def lims(points, alt=None):
        dm = margin(points, alt=alt)
        m, M = np.amin(points), np.amax(points)
        if alt is not None:
            m = min(m, np.amin(alt))
            M = max(M, np.amax(alt))
        return m - dm, M + dm

    connect = np.asarray(connect)
    coords = np.asarray(coords)
    # close off elements?
    co = co or connect.shape[1] > 2

    if len(coords.shape) == 1:
        coords = np.reshape(coords, (-1, 2))

    point_sets = [(coords, color, label)]
    altx = alty = None
    if overlay_coords is not None:
        if overlay_coords.shape != coords.shape:
            raise ValueError("coords and overlay_coords must have same shape")
        point_sets.append((overlay_coords, overlay_color, overlay_label))
        altx = overlay_coords[:, 0]
        alty = overlay_coords[:, 1]

    # determine limits for plot and plot the coords
    plt.xlim(lims(coords[:, 0], altx))
    plt.ylim(lims(coords[:, 1], alty))

    for (points, color, label) in point_sets:
        plt.scatter(
            points[:, 0], points[:, 1], color=color, edgecolor=color, label=label
        )
        # loop through elements and connect vertices with lines
        for (el, nodes) in enumerate(connect):
            for (i, b) in enumerate(nodes[1:], start=1):
                a = nodes[i - 1]
                x = [points[a, 0], points[b, 0]]
                y = [points[a, 1], points[b, 1]]
                plt.plot(x, y, color=color, linestyle="-")
            if co:
                # close out plot
                a = nodes[0]
                x = [points[a, 0], points[b, 0]]
                y = [points[a, 1], points[b, 1]]
                plt.plot(x, y, color=color, linestyle="-")

    plt.legend(loc="best")
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, transparent=True)
