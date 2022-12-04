from typing import Generator, Iterable

from tikzpaint.figures import Drawable, Displayable
from tikzpaint.util import copy, Number, Coordinates

from tikzpaint.shapes.displayable.arrow import L0Arrow

class Arrow(Drawable):
    """Implementation of an arrow that could be drawn on a figure"""
    def __init__(self, start: Coordinates | Iterable[Number], end: Coordinates | Iterable[Number]):
        self.start = Coordinates(start)
        self.end = Coordinates(end)
    
    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Arrow(self.start, self.end)
        return