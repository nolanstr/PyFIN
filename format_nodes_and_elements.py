import numpy as np


def FormatNodesAndElements(nodtab, eletab):
    
    dim, maxnod = 0, 0
    numele = len(eletab)
    elemap, eletyp = {}, []

    for (iel, eledef) in enumerate(eletab):
        eletyp.append(eledef[1])
        elemap[eledef[0]] = iel
        dim = max(dim, ElementDimension(eledef[1]))
        maxnod = max(maxnod, NodesPerElement(eledef[1]))

    eletyp = np.array(eletyp, dtype=int)
    
    nodmap = dict([(node[0],i) for (i, node) in enumerate(nodtab)])

    elecon = np.zeros((numele, maxnod), dtype=int)

    for (iel, eledef) in enumerate(eletab):
        nelnod = NodesPerElement(eletyp[iel])
        elecon[iel, :nelnod] = [nodmap[n] for n in eledef[2:]]
    
    numnod = len(nodtab)
    coord = np.zeros((numnod, dim))

    for (inode, node) in enumerate(nodtab):
        n = len(node[1:])
        coord[inode,:n] = node[1:]

    return nodmap, coord, elemap, eletyp, elecon


def NodesPerElement(eledef):
    #this will need to index the number of nodes
    return 2
def ElementDimension(eledef):
    #need update this to deal with elements with more than 2 dimensions
    return 3


