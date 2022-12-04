from abc import ABC
from abc import abstractmethod as virtual
from typing import Generator

from tikzpaint.figures.displayable import Displayable

# Drawable are objects that has the draw iterator - which is defined via repeatedly yielding displayables

class Drawable(ABC):
    """Base class for any object that could be displayed in the figure. 
    The implementation is essentially a wrapper for a displayable generator
    Drawables are layer 1 interactions with libraries, above displayables"""
    @virtual
    def draw(self)  -> Generator[Displayable, None, None]:
        pass