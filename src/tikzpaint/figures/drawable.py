from __future__ import annotations

from abc import ABC
from abc import abstractmethod as virtual
from typing import Generator
import numpy as np

from tikzpaint.figures.displayable import Displayable
from tikzpaint.util import Coordinates

# Drawable are objects that has the draw iterator - which is defined via repeatedly yielding displayables

class Drawable(ABC):
    """Base class for any object that could be displayed in the figure. 
    The implementation is essentially a wrapper for a displayable generator
    Drawables are layer 1 interactions with libraries, above displayables"""
    @virtual
    def draw(self)  -> Generator[Displayable, None, None]:
        pass

    def bound(self, bounds: float) -> Drawable:
        raise NotImplementedError(f"The bound method for {type(self).__name__} has not been implemented")