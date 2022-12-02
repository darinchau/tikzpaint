from tikzpaint.figures import Drawable, Displayable
from displayable.arrow import L0Arrow
from typing import Generator

class Arrow(Drawable):
    """Implementation of an arrow that could be drawn on a figure"""
    name = "Arrow"
    def __init__(self, start: tuple, end: tuple):
        self.start = start
        self.end = end
    
    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Arrow(self.start, self.end)
        return