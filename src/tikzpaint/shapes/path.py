from typing import Generator, Iterable
import numpy as np

from tikzpaint.figures import Drawable, Displayable 
from tikzpaint.util import Coordinates, copy, Number

from tikzpaint.shapes.displayable.path import L0Path

class Path(Displayable):
    """Implementation of an line that could be drawn on a figure
    
    *args: tuples of coordinate points"""
    def __init__(self, *args: Coordinates | Iterable[Number]):
        self.args = (Coordinates(a) for a in args)

    def draw(self) -> Generator[Displayable, None, None]:
        yield L0Path(list(self.args))
        return
