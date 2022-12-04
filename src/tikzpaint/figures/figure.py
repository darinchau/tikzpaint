from __future__ import annotations

from typing import Any
import matplotlib.pyplot as plt

from tikzpaint.util import copy, DECIMALS, num_parameters, notFalse
from tikzpaint.util import Coordinates

from tikzpaint.figures.drawable import Drawable
from tikzpaint.figures.displayable import Displayable
from tikzpaint.figures.projection import Projection
from tikzpaint.figures.options import Options

class Figure:
    """Figures stores all the thinks you are about to draw
    Available kwargs:
        - projection: Projection = defines a linear transformation from Rn to R2
        - round: bool = if set to false, then we will skip the rounding step
        - bound: Number = if given, then we will only draw stuff in the cube given by bounds centered at the origin, using the bounds method in every drawable"""
    def __init__(self, ndims: int = 2) -> None:
        self.toDraw : list[Displayable] = []
        self.ndims : int = ndims
    
    # output is true, then print, otherwise return the whole thing as a string
    def tikzify(self, output: bool = True, indentation: int = 4, scale: float = 0.7, **kwargs) -> str:
        """Output the tikz code"""

        if scale <= 0:
            raise ValueError(f"Scale must be greater or equal to 0, recieved {scale}")

        st = f"\\begin{{tikzpicture}}[scale={scale}]\n"
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
            for key, coord in dis.coordinates.items():
                if not isinstance(coord, Coordinates):
                    raise TypeError(f"The coordinate {key}: {coord} in {d} is not a coordinate point")
                
                if coord.n != self.ndims:
                    raise ValueError(f"The coordinate {key}: {coord} in {d} has incorrect number of dimensions ({len(coord)}) before projection, expects {self.ndims}")

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
                if not isinstance(self, Coordinates):
                    raise TypeError(f"The coordinate {key}: {val} in {d} is not a coordinate point")
                
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
                if notFalse(kwargs, "round"):
                    d.coordinates[key] = val = Coordinates(round(x, DECIMALS) for x in val)

                # Check dimensions
                if len(val) != 2:
                    raise ValueError(f"The coordinate {key}: {val} in {d} has incorrect number of dimensions: {len(val)}")
            
            # Make this a generator
            yield d