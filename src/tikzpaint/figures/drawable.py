from abc import ABC
from abc import abstractmethod as virtual
from typing import Generator, Any

# Displayable are objects that can be directly displayed on the figure
# Drawable are objects that has the draw iterator - which is defined via repeatedly yielding displayables

class Displayable(ABC):
    """Base class for any object that could be displayed in the figure"""
    name: str = "drawer"

    @virtual
    def __init__(self) -> None:
        """The init method will store all the necessary positional arguments such as coordinates to print etc"""
        raise NotImplementedError

    @virtual
    def tikzify(self, options: str) -> str:
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
    
    @virtual
    def __copy__(self):
        raise NotImplementedError

class Drawable(ABC):
    """Base class for any object that could be displayed in the figure"""
    @virtual
    def draw(self)  -> Generator[Displayable, None, None]:
        pass