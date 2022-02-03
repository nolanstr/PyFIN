import numpy as np

NEUMANN = 0
DIRICHLET = 1

def ApplyBoundaryConditionsUDOF(K, F, doftags, dofvals):

    if doftags.ndim == 1:
        doftags = doftags.reshape(-1,1)
        dofvals = dofvals.reshape(-1,1)
    
    numnod, ndof = doftags.shape
    Kbc, Fbc = K.copy(), F.copy()
    
    for i in range(numnod):
        for j in range(ndof):
            if doftags[i,j] == DIRICHLET:
                I = i * ndof + j
                Fbc -= [K[k,I] * dofvals[i,j] for k in range(numnod*ndof)]
                Kbc[I, :] = Kbc[:, I] = 0
                Kbc[I, I] = 1
    for i in range(numnod):
        for j in range(ndof):
            if doftags[i,j] == DIRICHLET:
                Fbc[i*ndof+j] = dofvals[i,j]

    return Kbc, Fbc

