from __future__ import annotations

from abc import ABC
from abc import abstractmethod as virtual
from typing import Generator, Any
import numpy as np

from tikzpaint.figures.displayable import Displayable
from tikzpaint.figures.options import PlotOptions
from tikzpaint.util import Coordinates

# Drawable are objects that has the draw iterator - which is defined via repeatedly yielding displayables

class Drawable(ABC):
    """Base class for any object that could be displayed in the figure. 
    The implementation is essentially a wrapper for a displayable generator
    Drawables are layer 1 interactions with libraries, above displayables"""
    @virtual
    def draw(self)  -> Generator[Displayable, None, None]:
        pass
    
    @property
    def option(self) -> PlotOptions:
        if not hasattr(self, "_options"):
            self._options = PlotOptions()
        return self._options
    
    def set_option(self, option_key: str, option_val: Any):
        """Sets the option with key to value. Returns self, so you might use method chaining if you wish"""
        self.option.__setattr__(option_key, option_val)
        return self