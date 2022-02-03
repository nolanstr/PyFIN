import numpy as np

def RemoveNearZeroValues(M, tol=1e-12):
    
    row, cols = np.where(abs(M) <= tol)
    M[row, cols] = 0

    return M
