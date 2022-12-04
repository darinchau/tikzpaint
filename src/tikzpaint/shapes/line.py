from typing import Generator
import numpy as np

from tikzpaint.figures import Drawable, Displayable, Number

from tikzpaint.shapes.vector import Vector
from tikzpaint.shapes.displayable.path import L0Path

class Line(Drawable):
    """Implementation of an line that could be drawn on a figure
    
    start: coordinates of the start of a line
    end: coordinates of the end of a line
    resolution: the resolution of a line such that if we perform stereographic projections and what nots we can get a curvy line"""
    name = "Arrow"
    def __init__(self, start: tuple[Number, ...], end: tuple[Number, ...], resolution: int = 100):
        self.start = start
        self.end = end
        if resolution < 1:
            raise ValueError(f"Resolution must be greater or equal to 1, recieved {resolution}")
        self.resolution = resolution
    
    def gen_coords(self) -> Generator[tuple[Number, ...], None, None]:
        for i in range(self.resolution + 1):
            start = np.array(self.start)
            end = np.array(self.end)
            res = start * (i / self.resolution) + end * (1 - i / self.resolution)
            yield tuple(float(x) for x in res)
        return

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Path(list(self.gen_coords()))
        return