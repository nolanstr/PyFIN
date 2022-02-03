import numpy as np


def stiffness(element_id, coords, area, youngs_modulus):
    """Computes the element stiffness for a 3D space truss member

    Parameters
    ----------
    coords : ndarray
        Nodal coordinates [[x1, y1, z1], [x2, y2, z2]]
    area : float
        Element area
    youngs_modulus : float
        Element elastic modulus

    Returns
    -------
    stiff : ndarray
        Element stiffness stored as a (ndof*2, ndof*2) symmetric matrix, where
        ndof is the number of degrees of freedom per node.
    """
    num_nodes = 2
    num_dof_per_node = 3
    
    v = coords[1] - coords[0]
    h = np.sqrt(np.dot(v, v))
    n = v / h
    nn = np.outer(n, n)
    
    stiff = np.zeros((num_nodes * num_dof_per_node, 
                            num_nodes * num_dof_per_node))
    
    i, j = num_dof_per_node, num_nodes * num_dof_per_node
    
    stiff[0:i, 0:i] = stiff[i:j, i:j] = nn
    stiff[0:i, i:j] = stiff[i:j, 0:i] = -nn

    return area * youngs_modulus / h * stiff
