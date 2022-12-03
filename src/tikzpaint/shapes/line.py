from typing import Generator

from tikzpaint.figures import Drawable, Displayable

from tikzpaint.shapes.vector import Vector
from tikzpaint.shapes.displayable.path import L0Path

class Line(Drawable):
    """Implementation of an line that could be drawn on a figure
    
    start: coordinates of the start of a line
    end: coordinates of the end of a line
    resolution: the resolution of a line such that if we perform stereographic projections and what nots we can get a curvy line"""
    name = "Arrow"
    def __init__(self, start: tuple, end: tuple, resolution: int = 100):
        self.start = start
        self.end = end
        self.resolution = resolution
    
    def gen_coords(self) -> Generator[tuple, None, None]:
        for i in range(self.resolution + 1):
            yield tuple(Vector(self.start).scale(i / self.resolution) + Vector(self.end).scale(1 - i / self.resolution))
        return

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Path(list(self.gen_coords()))
        return