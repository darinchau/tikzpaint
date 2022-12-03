from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod as virtual
from typing import TypeVar, Generic, Generator
from math import gcd

from tikzpaint.util import copy, isZero, Fraction, DECIMALS
from tikzpaint.figures import Drawable, Displayable

from tikzpaint.shapes.displayable.arrow import L0Arrow

_SupportArithmetic = TypeVar("_SupportArithmetic", int, Fraction, float)
class Vector(Drawable, Generic[_SupportArithmetic]):
    """Implementation of a vector that could be drawn on a canvas"""
    name = "Vector"
    def __init__(self, coords: tuple[_SupportArithmetic, ...] | Vector[_SupportArithmetic] | list[_SupportArithmetic]):
        self.__v = tuple(coords)

    def draw(self) -> Generator[Displayable, None, None]:
        coords = self.__v
        origin = tuple([0] * len(coords))
        yield L0Arrow(origin, coords)
        return
    
    def __getitem__(self, idx):
        return self.__v[idx]
    
    # Now Vector(tuple(v)) = tuple(Vector(v)) = v
    def __iter__(self):
        return iter(self.__v)
    
    def __len__(self):
        return len(self.__v)
    
    def __repr__(self):
        coords = []
        for v in self.__v:
            if isinstance(v, float):
                coords.append(str(round(v, DECIMALS)))
            else:
                coords.append(str(v))
        return "(" + ", ".join(coords) + ")"

    def __copy__(self):
        try:
            newv = [copy(v) for v in self.__v]
        except TypeError:
            newv = [v for v in self.__v]
        return Vector(newv)
    
    @property
    def magnitude(self) -> float:
        """The magnitude of the vector under Euclidean distance"""
        res: float = 0
        for x in self:
            res += float(x) * float(x)
        return np.sqrt(res)
        
    @property
    def normalized(self) -> Vector[float]:
        """The normalized vector"""
        return Vector([float(float(a) / self.magnitude) if self.magnitude != 0 else 0 for a in self.__v])
    
    @property
    def n(self):
        """Number of dimensions"""
        return len(self.__v)
    
    def scale(self, factor: _SupportArithmetic) -> Vector[_SupportArithmetic]:
        return Vector([a * factor if self.magnitude > 0 else 0 for a in self.__v]) # type: ignore
    
    @property
    def degree(self) -> _SupportArithmetic:
        s = 0
        for v in self.__v:
            s += v  # type: ignore
        return s # type: ignore

    def __add__(self, other: Vector[_SupportArithmetic]) -> Vector[_SupportArithmetic]:
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")
        return Vector([self[i] + other[i] for i in range(self.n)])
    
    def __sub__(self, other: Vector[_SupportArithmetic]) -> Vector[_SupportArithmetic]:
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")
        return Vector([self[i] - other[i] for i in range(self.n)])
    
    def __neg__(self) -> Vector[_SupportArithmetic]:
        return Vector([-self[i] for i in range(self.n)]) # type: ignore
    
    def __eq__(self, other: Vector[_SupportArithmetic]):
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")
        for i, j in zip(self.__v, other.__v, strict=True):
            if not isZero(i - j):
                return False
        return True
    
    def __hash__(self) -> int:
        return hash(self.__v)
    
    def dot(self, other: Vector[_SupportArithmetic]) -> _SupportArithmetic:
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")
        sum = 0
        for vi, wi in zip(self.__v, other.__v):
            sum = sum + vi * wi # type: ignore
        return sum # type: ignore
    
    def project(self, target: Vector):
        if not self.n == target.n:
            raise ValueError("The two vectors are of different length")
        return target.scale(target.dot(self) / target.dot(target)) # type: ignore
    
    def distBetween(self, other) -> float:
        if not isinstance(other, Vector):
            raise TypeError(f"distance operation not supported between vector and {type(other).__name__}")
        if not self.n == other.n:
            raise ValueError("The two vectors are of different length")
        return (self - other).magnitude

    @classmethod
    def canonicalBasis(cls, idx: int, ambient_dims: int):
        """This subtracts one for index, that means we start counting from 1 to n"""
        idx -= 1
        if 0 <= idx < ambient_dims:
            return Vector([1 if i == idx else 0 for i in range(ambient_dims)])
        raise ValueError(f"The index ({idx}) must be between 1 and {ambient_dims}")
    
    @classmethod
    def zeroVector(cls, ambient_dims: int):
        return Vector([0 for _ in range(ambient_dims)])