from typing import Generator, Iterable

from tikzpaint.figures import Drawable, Displayable 
from tikzpaint.util import Coordinates, copy, Number

from tikzpaint.shapes.displayable.point import L0Point

class Point(Drawable):
    """Implementation of a point that can be drawn on the figure
    
    p: the coordinates of said point"""
    def __init__(self, p: Coordinates | Iterable[Number]):
        self.p = Coordinates(p)

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Point(self.p)
        return
