from typing import Generator

from tikzpaint.figures import Drawable, Displayable, Number

from tikzpaint.shapes.displayable.point import L0Point

class Point(Drawable):
    """Implementation of a point that can be drawn on the figure
    
    p: the coordinates of said point"""
    name = "Arrow"
    def __init__(self, p: tuple[Number, ...]):
        self.p = p

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Point(self.p)
        return