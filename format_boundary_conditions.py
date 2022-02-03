import numpy as np

ALL = ''
BOUNDARY = ''
ILO, IHI, JLO, JHI, KLO, KHI = '', '', '', '', '', ''
MAG = 1


def FormatBoundaryConditions(coords, nodmap, elecon, eletyp, bcs, cloads=None):
    
    cloads = cloads or []
    numnod, numdim = coords.shape
    MDOF = coords.shape[1]
    doftags = np.zeros((numnod, MDOF), dtype=int)
    dofvals = np.zeros((numnod, MDOF))

    directions = {'X':0,
                  'Y':1,
                  'Z':2,
                  'ALL':[0,1,2]}
    
    for (itype, uitem) in enumerate((cloads, bcs)):
            for (label, dof, mag) in uitem:

                if isinstance(label, int):
                    inodes = [nodmap[label]]
                elif label == 'ALL':
                    inodes = range(numnod)
                elif label == BOUNDARY:
                    inodes = BoundaryNodes(coords, elecon, eletyp)
                elif label in (ILO, IHI, JLO, JHI, KLO, KHI):
                    inodes = NodesInRectilinearRegion(coords, label)
                else:
                    inodes = [nodmap[xn] for xn in label]
                
                if dof == 'ALL':
                    dofs = directions[dof]
                else:
                    dofs = [directions[dof_i] for dof_i in dof]
                
                magnitude = mag                

                if not IsListLike(magnitude):
                    magnitude = np.ones(len(inodes)) * magnitude

                for (i, inode) in enumerate(inodes):
                    for j in dofs:
                        doftags[inode, j] = itype
                        dofvals[inode, j] = float(magnitude[i])

    return doftags, dofvals


def BoundaryNodes(coords, elecon, eletyp):
    return []
def NodesInRectilinearRegion(coords, label):
    return []
def IsListLike(dof):
    return False
