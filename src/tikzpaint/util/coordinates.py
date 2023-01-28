from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod as virtual
from typing import TypeVar, Generic, Generator, Iterator, Iterable
from math import gcd

from tikzpaint.util.utils import copy, isZero
from tikzpaint.util.constants import DECIMALS

Number = TypeVar("Number", int, float, np.int64, np.float64, np.int32, np.integer, np.floating)

class Coordinates(tuple):
    """A tuple with loads of coordinates method which serves as the base type for most stuff here"""
    def __new__(cls, it: Iterable[Number]):
        newargs = (float(a) for a in it)
        return super().__new__(cls, newargs)
    
    def __iter__(self) -> Iterator[float]:
        return super().__iter__()
    
    @property
    def magnitude(self) -> float:
        """The magnitude of the coordinates from the origin under Euclidean distance"""
        res: float = 0
        for x in self:
            res += float(x) * float(x)
        return np.sqrt(res)
        
    def normalized(self) -> Coordinates:
        """Returns the point on the unit ball thats one unit length away from the origin but in the same direction as usual
        If the magnitude of the vector is 0 then returns the zero vector"""
        if isZero(self.magnitude, strict=True):
            return Coordinates(0 for _ in self)
        return Coordinates(float(x / self.magnitude) for x in self)
    
    @property
    def n(self):
        """float of dimensions"""
        return len(self)
    
    def scale(self, factor: Number)  -> Coordinates:
        """Creates a new copy that is a scaled vector with respect to the origin"""
        return Coordinates(float(x * factor) if self.magnitude > 0 else 0 for x in self)
    
    def checkLength(self, other: Coordinates):
        """Raises and error if self and other has different length"""
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")

    @property
    def degree(self) -> float:
        """Returns the sum of all the entries in self"""
        return sum(self)

    def __add__(self, other: Coordinates) -> Coordinates:
        self.checkLength(other)
        return Coordinates(float(self[i] + other[i]) for i in range(self.n))
    
    def __sub__(self, other: Coordinates) -> Coordinates:
        self.checkLength(other)
        return Coordinates(float(self[i] - other[i]) for i in range(self.n))
    
    def __rmul__(self, other: Number):
        return self.scale(other)
    
    def __neg__(self) -> Coordinates:
        return Coordinates(float(-self[i]) for i in range(self.n))
    
    def __eq__(self, other: Coordinates):
        self.checkLength(other)
        return np.allclose(np.array(self), np.array(other))
    
    def dot(self, other: Coordinates) -> float:
        self.checkLength(other)
        return float(np.dot(np.array(self), np.array(other)))
    
    def project(self, target: Coordinates):
        self.checkLength(target)
        return target.scale(target.dot(self) / target.dot(target))
    
    def distBetween(self, other: Coordinates) -> float:
        self.checkLength(other)
        return (self - other).magnitude

    @classmethod
    def canonicalBasis(cls, idx: int, ambient_dims: int):
        """
        Returns the i-th axis
        This subtracts one for index, that means we start counting from 1 to n"""
        idx -= 1
        if 0 <= idx < ambient_dims:
            return Coordinates(float(1) if i == idx else 0 for i in range(ambient_dims))
        raise ValueError(f"The index ({idx + 1}) must be between 1 and {ambient_dims}")
    
    @classmethod
    def origin(cls, ambient_dims: int):
        return Coordinates(0 for _ in range(ambient_dims))
