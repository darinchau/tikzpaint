from abc import ABC
from abc import abstractmethod as virtual
import numpy as np
from typing import TypeVar, TypeAlias, Any
from tikzpaint.util import Coordinates

# Displayable are objects that can be directly displayed on the figure

class Displayable(ABC):
    """Base class for any object that could be displayed in the figure
    Displayables are the layer 0 interaction between external libraries (such as matplotlib or tikz) and your code
    Displayables should only draw really really basic stuff such as a line or an arrow or a point"""

    @virtual
    def __init__(self) -> None:
        """The init method will store all the necessary positional arguments such as coordinates to print etc"""
        raise NotImplementedError

    @virtual
    def tikzify(self) -> str:
        """The tikz command to draw"""
        raise NotImplementedError
    
    @virtual
    def plot(self):
        """Plots the figure on a GUI using matplotlib"""
        raise NotImplementedError
    
    @property
    def coordinates(self):
        if not hasattr(self, "_coordinates") or self._coordinates is None:
            self._coordinates: dict[Any, Coordinates] = {}
        return self._coordinates
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options: list[str] = []
        return self._options

    @property
    def tikz_options(self) -> str:
        return ", ".join(self.options)
    
    @virtual
    def __copy__(self):
        raise NotImplementedError