import numpy as np
from tikzpaint.util.constants import NDArray
from tikzpaint.util.coordinates import Coordinates

def get_orthonormal_basis(t: Coordinates) -> NDArray:
    v = np.array(t)
    M = np.concatenate([v.reshape(-1, 1), np.eye(len(t))], axis = 0)
    q, r = np.linalg.qr(M)
    return q