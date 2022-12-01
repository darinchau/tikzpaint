from abc import ABC
import numpy as np
from typing import Callable, Any
import matplotlib.pyplot as plt
from inspect import signature
from tikzpaint.util import copy, DECIMALS, num_parameters
from drawable import Drawable, Displayable

class Projection(ABC):
    """Projection function object useful for defining projections of coordinates"""
    def __init__(self, *args: Callable):
        self.input_dims = num_parameters(args[0])
        self.result_dims = len(args)
        self.fns = list(args)
    
    def __call__(self, t: tuple):
        res = (self.fns[i](*t) for i in range(self.result_dims))
        return tuple(res)

class Figure:
    """This helps me draw tikz stuff"""
    def __init__(self, ndims: int = 2) -> None:
        self.toDraw : list[Displayable | Drawable] = []
        self.ndims : int = ndims
    
    ## TODO make generation of lines and stuff dynamic with type check
    # output is true, then print, otherwise return the whole thing as a string
    # Bounds defines the bounding n-cube for the drawing
    def tikzify(self, output: bool = True, indentation: int = 4, **kwargs) -> str:
        """Output the tikz code"""   

        st = "\\begin{tikzpicture}[scale=0.7]\n"
        for d in self._preprocess(kwargs):
            options = ", ".join(self.options + d.options)
            st += " " * indentation + d.tikzify(options) + "\n"
        st += "\\end{tikzpicture}"

        # Print the whole thing if needed
        if output:
            print(st)
        
        return st
    
    def plot(self, **kwargs):
        """Output the figure"""

        plt.figure()
        for d in self._preprocess(kwargs):
            d.plot()
        
        plt.show()
        plt.clf()

        return
    

    def draw(self, d: Drawable | Displayable) -> None:
        """Add something to draw in tikz code"""
        if isinstance(d, Drawable) or isinstance(d, Displayable):
            self.toDraw.append(d)
        else:
            raise TypeError(f"{d} is not a drawable or displayable object")
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options: list[str] = []
        return self._options

    # Naively loop through all displayables in self.todraw, without checking
    def _iter_raw(self):
        for d in self.toDraw:
            if isinstance(d, Displayable):
                yield copy(d)
            elif isinstance(d, Drawable):
                for dis in d.draw():
                    yield copy(dis)
    
    def _preprocess(self, kwargs: dict[str, Any]):
        for d in self._iter_raw():
            for key, val in d.coordinates.items():
                
                # Check type
                if type(val) != tuple:
                    raise TypeError(f"The coordinate {key}: {val} in {d} is not a tuple")
                
                if len(val) != self.ndims:
                    raise ValueError(f"The coordinate {key}: {val} in {d} has incorrect number of dimensions before projection: {len(val)}")

                # Perform projection
                if "projection" in kwargs:
                    proj: Projection = kwargs["projection"]
                    if not proj.result_dims == 2:
                        raise ValueError("Output of projection dimensions must be 2")
                    if not proj.input_dims == self.ndims:
                        raise ValueError(f"Input of projection dimensions must be {self.ndims}")
                    d.coordinates[key] = val = proj(val)
                
                # Perform rounding by default unless explicitly set to false
                if not "round" in kwargs or kwargs["round"]:
                    d.coordinates[key] = val = tuple([round(v, DECIMALS) for v in val])
                
                # Check dimensions
                if len(val) != 2:
                    raise ValueError(f"The coordinate {key}: {val} in {d} has incorrect number of dimensions: {len(val)}")
            
            # Make this a generator
            yield d