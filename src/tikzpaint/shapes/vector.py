from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod as virtual
from typing import TypeVar, Generic, Generator
from math import gcd

from tikzpaint.util import copy, isZero, DECIMALS
from tikzpaint.util import Number, Coordinates
from tikzpaint.figures import Drawable, Displayable

from tikzpaint.shapes.base.arrow import L0Arrow

class Vector(Drawable, Coordinates):
    """Implementation of a vector that could be drawn on a canvas"""
    def draw(self) -> Generator[Displayable, None, None]:
        origin = Coordinates([0] * len(self))
        yield L0Arrow(origin, self)
        return
    
    def bound(self, bounds: float) -> Vector:
        """This method helps us take care of the bounding separately
        the bounds denotes a cube around the origin, the range which we will draw"""
        the_max = max([abs(x) for x in self])
        if the_max <= bounds:
            return Vector(self)
        return Vector(self.scale(bounds/the_max))
