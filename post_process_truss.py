import numpy as np

def TrussIntForces(coord, elecon, elemat, elefab, u, nodmap):
    p = np.zeros(elecon.shape[0])
    for (e, c) in enumerate(elecon):
        c = [nodmap[n] for n in c]
        p[e] = Link2IntForce(coor[c], elemat[e], elefab[e], u[c])
    return p

def Link2IntForce(xc, E, A, uc):
    x = xc[1] - xc[0]
    u = uc[1] - uc[0]
    Xu = np.dot(x, u)
    L = np.sqrt(dot(x, x))
    return E * A / L * Xu / L

def TrussStresses(p, elefab):
    return p / elefab

def WriteFEResults(job_id, coord, nodmap, elemap, eletyp, elecon, u, **kwargs):
    '''
    this will eventually need to write results to a vtk finite element database
    such that ParaView  can use it.
    '''
    return None
