from __future__ import annotations

from typing import Any
import numpy as np

from matplotlib.figure import Figure as matplotlibFigure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from tikzpaint.util import copy, DECIMALS, num_parameters, notFalse
from tikzpaint.util import NDArray
from tikzpaint.util import Coordinates

from tikzpaint.figures.drawable import Drawable
from tikzpaint.figures.displayable import Displayable
from tikzpaint.figures.projection import Projection
from tikzpaint.figures.options import PlotOptions

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
    
    def plot(self, show: bool = True, process_img: bool = False, off_axis: bool = True, bound: float = -1, **kwargs):
        """Output the figure
        
        - show: bool = if set to true, then we will display the image, otherwise we wont
        - process_img: bool = if set to true, then we will return the image of the plot in this function.
        - off_axis: bool = if set to True, then the axis will not appear in the resulting image
        - bound: float = if -1, then there are no bounds, otherwise we restrict our view to (-a, a) on both x and y axis"""

        fig = plt.figure()   

        ax = fig.gca()     

        for d in self.preprocess(kwargs):
            d.plot(ax)
            
        
        if bound >= 0:
            ax.set_xbound(-bound, bound)
            ax.set_ybound(-bound, bound)
        
        arr = None

        if process_img:
            arr = mpl_to_np(fig, off_axis)
        
        if show:
            plt.show(block = True)

        fig.clf()
        plt.close(fig)
        
        return arr
    
    def _draw(self, d: Drawable) -> None:
        """Draw one thing at a time"""
        # Perform one checking first
        for dis in d.draw():
            for key, coord in dis.coordinates.items():
                if not isinstance(coord, Coordinates):
                    raise TypeError(f"The coordinate {key}: {coord} in {type(d).__name__} is not a coordinate point, recieved {type(coord).__name__}")
                
                if coord.n != self.ndims:
                    raise ValueError(f"The coordinate {key}: {coord} in {type(d).__name__} has incorrect number of dimensions ({len(coord)}) before projection, expects {self.ndims}")

        # Only append if everything passes the check   
        for dis_ in d.draw():
            dis = copy(dis_)
            dis._set_options(d.option)
            self.toDraw.append(dis)
    
    def draw(self, *d: Drawable):
        """Registers the drawable onto the drawing board, for rendering later
        - d: the drawable object to be drawn"""
        for drawable in d:
            self._draw(drawable)
    
    @property
    def options(self):
        if not hasattr(self, "_options") or self._options is None:
            self._options: list[str] = []
        return self._options
    
    def preprocess(self, kwargs: dict[str, Any]):
        for d_ in self.toDraw:

            # Make a copy first to avoid modification of the original
            d = copy(d_)

            for key, coord in d.coordinates.items():
                # Check type
                if not isinstance(coord, Coordinates):
                    raise TypeError(f"The coordinate {key}: {coord} in {type(d).__name__} is not a coordinate point, recieved {type(coord).__name__}")
                
                # Check length of coordinates
                if len(coord) != self.ndims:
                    raise ValueError(f"The coordinate {key}: {coord} in {d} has incorrect number of dimensions before projection: {len(coord)}")

                # Perform projection
                if "projection" in kwargs:
                    proj: Projection = kwargs["projection"]
                    if not proj.result_dims == 2:
                        raise ValueError(f"Output of projection dimensions must be 2, recieved {proj.result_dims} instead")
                    if not proj.input_dims == self.ndims:
                        raise ValueError(f"Input of projection dimensions must be {self.ndims}, recieved {proj.input_dims} instead")
                    d.coordinates[key] = coord = proj(coord)
                
                # Perform rounding by default unless explicitly set to false
                if notFalse(kwargs, "round"):
                    d.coordinates[key] = coord = Coordinates(round(x, DECIMALS) for x in coord)

                # Check dimensions
                if len(coord) != 2:
                    raise ValueError(f"The coordinate {key}: {coord} in {d} has incorrect number of dimensions: {len(coord)}")
            
            # Make this a generator
            yield d


def mpl_to_np(fig: matplotlibFigure, offaxis: bool = True) -> NDArray[np.uint8]:
    """Converts a matplotlib figure to a RGB frame after updating the canvas."""

    canvas = FigureCanvasAgg(fig)
    if offaxis:
        ax = fig.gca()
        ax.axis('off')
    canvas.draw()  # update/draw the elements

    # get the width and the height to resize the matrix
    l, b, w, h = canvas.figure.bbox.bounds # type: ignore
    w, h = int(w), int(h)

    #  exports the canvas to a string buffer and then to a numpy nd.array
    buf = canvas.tostring_rgb()
    image = np.frombuffer(buf, dtype=np.uint8) # type: ignore
    return image.reshape(h, w, 3)