import numpy as np
from tikzpaint.util.constants import NDArray
from tikzpaint.util.coordinates import Coordinates

def cross(u: Coordinates, v: Coordinates):
    assert u.n == 3
    assert v.n == 3

    return Coordinates((u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]))

def get_orthonormal_basis(t: Coordinates) -> NDArray:
    v = np.array(t)
    M = np.concatenate([v.reshape(-1, 1), np.eye(len(t))], axis = 1)
    q, r = np.linalg.qr(M)
    return q
