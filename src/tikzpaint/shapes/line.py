from typing import Generator, Iterable
import numpy as np

from tikzpaint.figures import Drawable, Displayable
from tikzpaint.util import Coordinates, copy, Number

from tikzpaint.shapes.vector import Vector
from tikzpaint.shapes.base import L0Path

class Line(Drawable):
    """Implementation of an line that could be drawn on a figure
    
    start: coordinates of the start of a line
    end: coordinates of the end of a line
    resolution: the resolution of a line such that if we perform stereographic projections and what nots we can get a curvy line"""
    def __init__(self, start: Coordinates | Iterable[Number], end: Coordinates | Iterable[Number], resolution: int = 100):
        self.start = Coordinates(start)
        self.end = Coordinates(end)
        if resolution < 1:
            raise ValueError(f"Resolution must be greater or equal to 1, recieved {resolution}")
        self.resolution = resolution
    
    def gen_coords(self) -> Generator[Coordinates, None, None]:
        for i in range(self.resolution + 1):
            yield self.start.scale(i / self.resolution) + self.end.scale(1 - i / self.resolution)
        return

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Path(list(self.gen_coords()))
        return
    
    @classmethod
    def StraightLine(cls, start: Coordinates | Iterable[Number], end: Coordinates | Iterable[Number]):
        return cls(start, end, resolution = 1)