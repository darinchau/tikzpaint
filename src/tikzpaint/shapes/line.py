from tikzpaint.figures import Drawable, Displayable
from displayable.line import L0Line
from typing import Generator

class Line(Drawable):
    """Implementation of an line that could be drawn on a figure"""
    name = "Arrow"
    def __init__(self, start: tuple, end: tuple):
        self.start = start
        self.end = end
    
    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Line(self.start, self.end)
        return