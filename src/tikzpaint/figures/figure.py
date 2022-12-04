from __future__ import annotations

from abc import ABC
import numpy as np
from typing import Callable, Any, Generator
import matplotlib.pyplot as plt
from inspect import signature

from tikzpaint.util import copy, DECIMALS, num_parameters

from tikzpaint.figures.drawable import Drawable
from tikzpaint.figures.displayable import Displayable
from tikzpaint.figures.projection import Projection

class Figure:
    """Figures stores all the thinks you are about to draw
    Available kwargs:
        - projection: A Projection functions object that defines a linear transformation from Rn to R2"""
    def __init__(self, ndims: int = 2) -> None:
        self.toDraw : list[Displayable] = []
        self.ndims : int = ndims
    
    # output is true, then print, otherwise return the whole thing as a string
    def tikzify(self, output: bool = True, indentation: int = 4, **kwargs) -> str:
        """Output the tikz code"""

        st = "\\begin{tikzpicture}[scale=0.7]\n"
        for d in self.preprocess(kwargs):
            st += " " * indentation + d.tikzify() + "\n"
        st += "\\end{tikzpicture}"

        # Print the whole thing if needed
        if output:
            print(st)
        
        return st
    
    def plot(self, **kwargs):
        """Output the figure"""

        plt.figure()
        for d in self.preprocess(kwargs):
            d.plot()
        
        plt.show()
        plt.clf()

        return
    

    def draw(self, d: Drawable) -> None:
        """Add something to draw in tikz code"""
        # Perform one checking first
        for dis in d.draw():
            for key, val in dis.coordinates.items():
                if type(val) != tuple:
                    raise TypeError(f"The coordinate {key}: {val} in {d} is not a tuple")
                
                if len(val) != self.ndims:
                    raise ValueError(f"The coordinate {key}: {val} in {d} has incorrect number of dimensions before projection: {len(val)}")

        # Only append if everything passes the check   
        for dis in d.draw(): 
            self.toDraw.append(copy(dis))
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options: list[str] = []
        return self._options
    
    def preprocess(self, kwargs: dict[str, Any]):
        for d_ in self.toDraw:

            # Make a copy first to avoid modification of the original
            d = copy(d_)

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
                        raise ValueError(f"Output of projection dimensions must be 2, recieved {proj.result_dims} instead")
                    if not proj.input_dims == self.ndims:
                        raise ValueError(f"Input of projection dimensions must be {self.ndims}, recieved {proj.input_dims} instead")
                    d.coordinates[key] = val = proj(val)
                
                # Perform rounding by default unless explicitly set to false
                if not "round" in kwargs or kwargs["round"]:
                    d.coordinates[key] = val = tuple([round(v, DECIMALS) for v in val])
                
                # Check dimensions
                if len(val) != 2:
                    raise ValueError(f"The coordinate {key}: {val} in {d} has incorrect number of dimensions: {len(val)}")
            
            # Make this a generator
            yield d