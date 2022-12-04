from typing import Generator
import numpy as np

from tikzpaint.figures import Drawable, Displayable, Number

from tikzpaint.shapes.displayable.path import L0Path

class Path(Displayable):
    """Implementation of an line that could be drawn on a figure
    
    *args: tuples of coordinate points"""
    name = "Arrow"
    def __init__(self, *args: tuple[Number, ...]):
        self.args = args

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Path(list(self.args))
        return