from __future__ import annotations

from abc import ABC
from abc import abstractmethod as virtual
from typing import Callable, Any
import matplotlib.pyplot as plt
from inspect import signature
import numpy as np

from tikzpaint.util import copy, NDArray, to_superscript, isZero, get_orthonormal_basis
from tikzpaint.util import Coordinates, Number

class Projection(ABC):
    @property
    @virtual
    def input_dims(self) -> int:
        raise NotImplementedError
    
    @property
    @virtual
    def result_dims(self) -> int:
        raise NotImplementedError
    
    @virtual
    def __call__(self, t: Coordinates) -> Coordinates:
        raise NotImplementedError
    
    @virtual
    def __copy__(self):
        raise NotImplementedError

    def combine(self, p2: Projection):
        class MixedProjection(Projection):
            # THis constructor is private
            def __init__(self, p1: Projection, p2: Projection):
                if not p1.result_dims == p2.input_dims:
                    raise ValueError(f"The output dimensions f p1 ({p1.result_dims}) is not the same as the input dimensions of p2 ({p2.input_dims})")
                self.p1 = p1
                self.p2 = p2
            
            def input_dims(self) -> int:
                return self.p1.input_dims
            
            def result_dims(self) -> int:
                return self.p2.result_dims
            
            def __call__(self, t: Coordinates) -> Coordinates:
                t = self.p1(t)
                return self.p2(t)
            
            def __copy__(self):
                return MixedProjection(copy(self.p1), copy(self.p2))
        
        return MixedProjection(self, p2)


class LinearProjection(Projection):
    """Projection is a function object useful for defining projections of coordinates
    array: the matrix for the linear projection"""
    def __init__(self, array: NDArray):
        if not len(array.shape) == 2:
            raise ValueError(f"The array should be in 2 dimensions, recieved an array with shape {array.shape} instead")
        self.matrix = copy(array)

    @property
    def input_dims(self):
        return self.matrix.shape[1]

    @property
    def result_dims(self):
        return self.matrix.shape[0]
    
    def __call__(self, t: Coordinates) -> Coordinates:
        v = np.array(t)
        if v.shape[0] != self.input_dims:
            raise ValueError(f"The length of t is expected to be ({self.input_dims}), got ({v.shape}) instead")
        v = self.matrix @ v
        # Cast back to default float to avoid shenanigans
        return tuple(float(x) for x in v)
    
    def __copy__(self):
        return LinearProjection(self.matrix)
    
    @classmethod
    def fromNormalVector(cls, t: Coordinates):
        """Creates a linear projection from Rn to Rn-1 with normal vector t"""
        # Use the gram-shit process
        q = get_orthonormal_basis(t)
        return LinearProjection(q[1:, :])
    
    def combine(self, p2: LinearProjection):
        """Combines the linear projection self and p2, performing self first then p2"""
        if not self.result_dims == p2.input_dims:
            raise ValueError(f"The output dimensions of self ({self.result_dims}) is not the same as the input dimensions of p2 ({p2.input_dims})")
        return LinearProjection(p2.matrix @ self.matrix)
    
    @classmethod
    def scale(cls, scales: tuple[Number, ...]):
        """Scales the whole space according to the scales tuple on each dimension."""
        m = np.eye(len(scales))
        for i, s in enumerate(scales):
            m[i][i] = s
        return LinearProjection(m)


def project(t1: Coordinates, t2: Coordinates):
    """Returns the projection of t1 to the span of t2"""
    v1 = np.array(t1)
    v2 = np.array(t2)
    return (v1 @ v2)/(v2 @ v2) * v2

def magnitude(t: Coordinates) -> float:
    """Returns the magnitude of a vector"""
    v = np.array(t)
    return float(np.sqrt(np.sum(v ** 2)))

class StereographicProjection(Projection):
    def __init__(self, n: int) -> None:
        """Defines a stereographic projection from (1, 0, ..., 0) from Sn+1 to Rn"""
        self.n = n
    
    @property
    def input_dims(self) -> int:
        return self.n
    
    @property
    def result_dims(self) -> int:
        return self.n - 1
    
    def __copy__(self):
        return StereographicProjection(self.n)
    
    def __call__(self, t: Coordinates) -> Coordinates:
        if not isZero(magnitude(t) - 1):
            raise ValueError(f"t: {t} is not a point on the unit sphere in R{to_superscript(self.n)}")
        if t[0] == 1:
            t = (0.999, 0.0019999) + t[2:]
        return tuple(x / (1 - t[0]) for x in t[1:])
    
    @staticmethod
    def fromOrigin(origin: Coordinates):
        stereo = StereographicProjection(len(origin))
        # First make the origin to (1, 0, 0, ...)
        scale = LinearProjection.scale(tuple(1/ magnitude(origin) for _ in origin))
        