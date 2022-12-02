from abc import ABC
from abc import abstractmethod as virtual
from typing import Any

# Displayable are objects that can be directly displayed on the figure
# Drawable are objects that has the draw iterator - which is defined via repeatedly yielding displayables

class Displayable(ABC):
    """Base class for any object that could be displayed in the figure
    Displayables are the layer 0 interaction between external libraries (such as matplotlib or tikz) and your code
    Displayables should only draw really really basic stuff such as a line or an arrow or a point"""
    name: str = "drawer"

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
            self._coordinates: dict[Any, tuple] = {}
        return self._coordinates
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options: list[str] = []
        return self._options

    @property
    def tikz_options(self) -> str:
        return ""
    
    @virtual
    def __copy__(self):
        raise NotImplementedError