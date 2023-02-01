from __future__ import annotations

from abc import ABC
from abc import abstractmethod as virtual
import numpy as np
from typing import Any, ParamSpec, Callable, Generator
from tikzpaint.util import Coordinates, copy
from tikzpaint.figures.options import PlotOptions
from matplotlib.axes import Axes


# Displayable are objects that can be directly displayed on the figure
class Displayable:
    """Base class for any object that could be displayed in the figure
    Displayables are the layer 0 interaction between external libraries (such as matplotlib or tikz) and your code
    We have displayables only for basic tikz commands"""

    @virtual
    def __init__(self) -> None:
        """The init method will store all the necessary positional arguments such as coordinates to print etc"""
        raise NotImplementedError

    @virtual
    def tikzify(self) -> str:
        """The tikz command to draw"""
        raise NotImplementedError
    
    @virtual
    def plot(self, fig: Axes):
        """Plots the figure on a GUI using matplotlib"""
        raise NotImplementedError
    
    @property
    def coordinates(self):
        if not hasattr(self, "_coordinates") or self._coordinates is None:
            self._coordinates: dict[str | int, Coordinates] = {}
        return self._coordinates
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options = PlotOptions()
        return self._options

    @property
    def tikz_options(self) -> str:
        return self.options.to_tikz()
    
    @virtual
    def __copy__(self):
        raise NotImplementedError
    
    @virtual
    def pathify(self) -> Generator[Displayable, None, None]:
        """This method is designed for non-linear projections. In this method you transform your object into a series of paths and points
        such that they can be used with non-linear projections."""
        raise NotImplementedError
