import numpy as np
from .global_stiffness import * 
from .global_force import * 
from .format_boundary_conditions import *
from .format_nodes_and_elements import *
from .apply_boundary_conditions import *
from .post_process_truss import *
from .post_process_results import *

def TrussSolution(nodtab, eletab, elemat, elefab, 
                        bcs, c_loads, job_id='Job-1'):
    """Computes the solution for a 3D space truss

    Parameters
    ----------
    coords : ndarray
        Nodal coordinates [[x1, y1, z1], [x2, y2, z2]]
    connects : ndarray
        
    area : float
        Element area
    youngs_modulus : float
        Element elastic modulus

    Returns
    -------

    """
    
    nodmap, coord, elemap, eletyp, elecon = FormatNodesAndElements(nodtab,
                                                                        eletab)
    
    numele, numnod = elecon.shape[0], coord.shape[0]
    ndof = 1 if coord.ndim == 1 else coord.shape[1]
    
    doftags, dofvals = FormatBoundaryConditions(coord, nodmap, eletyp, elecon,
                                                                    bcs, c_loads)
    doftags, dofvals = doftags[:,:ndof], dofvals[:,:ndof]

    K = assemble(coord, elecon, elefab, elemat)
    F,Q = AssembleGlobalForceUDOF(coord, elemap, eletyp, elecon, doftags,
                                                                    dofvals)
    Kbc, Fbc = ApplyBoundaryConditionsUDOF(K, F+Q, doftags, dofvals)
    
    try:
        u = np.linalg.solve(Kbc, Fbc)
    except:
        raise RuntimeError('attamping to solve under constrained system')

    Ft = np.dot(K, u)
    R = Ft - F - Q
    u, R = u.reshape(coord.shape), R.reshape(coord.shape)
    R = RemoveNearZeroValues(R)
    
    return u, R
