import numpy as np

NEUMANN = 0

def AssembleGlobalForceUDOF(coord, elemap, eletyp, elecon, doftags, dofvals,
                                    f=None):
    
    if doftags.ndim == 1:
        doftags = dogtags.reshape((-1,1))
        dofvals = dofvals.reshape((-1,1))

    coord, elecon = np.asarray(coord), np.asarray(elecon)

    numnod = coord.shape[0]
    ndof = NumberOfDOFPerNode(eletyp[0])

    Q = np.array([dofvals[i,j] if doftags[i,j] == NEUMANN else 0. \
                                for i in range(numnod) for j in range(ndof)])
    F = np.zeros(ndof*numnod)
    
    for (e, c) in enumerate(elecon):
        c = c[:NodesPerElement(eletyp[e])]
        fc = np.zeros(len(c)) if f is None else f[c]
        args = (coord[c], fc)

        #if dltags is not None:
            #args += (dltags[e], dlvals[e])

        Fe = ElementForce(eletyp[e], *args)

        if Fe is None:
            xel = elemap.keys()[elemap.values().index(iel)]
            raise ValueError('Element %d has unknown element type' % xel)

        eft = np.array([[(ndof*ni) + i for i in range(ndof)] for ni in \
                                                                c]).flatten()

        for i in range(Fe.shape[0]):
            F[eft[i]] += Fe[i]

    return F, Q
            

def NumberOfDOFPerNode(eletyp):
    return 3

def NodesPerElement(eletyp):
    return 2
def ElementForce(eletype, *args):
    return np.zeros(1)
