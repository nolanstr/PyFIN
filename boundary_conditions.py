import numpy as np


def apply_boundary_conditions(K, F, coords, connects, bcs):

    Fbc, Kbc = F.copy, K.copy

    n_nodes, ndof = coords.shape
    
    for i in range(n_nodes):
        for j in range(ndof):

            idx = (i * ndof) + j 


    return bc
