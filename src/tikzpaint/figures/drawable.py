from abc import ABC
from abc import abstractmethod as virtual
from typing import Generator, Any
from displayable import Displayable

class Drawable(ABC):
    """Base class for any object that could be displayed in the figure. 
    The implementation is essentially a wrapper for a displayable generator
    Drawables are layer 1 interactions with libraries, above displayables"""
    @virtual
    def draw(self)  -> Generator[Displayable, None, None]:
        pass