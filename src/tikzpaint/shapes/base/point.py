from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Any, Generator

class L0Point(Displayable):
    """Implementation of a point that could be drawn on a figure"""
    def __init__(self, p: Coordinates):
        self.coordinates[""] = copy(p)
    
    def tikzify(self):
        p = self.coordinates[""]
        return f"\\node[{self.tikz_options}] at {p} {{}}"

    def plot(self, ax: Axes):
        x, y = self.coordinates[""]
        ax.plot(x, y, 
            marker="o", 
            markersize=self.options.width * 10, 
            markeredgecolor=self.options.pltcolor, 
            markerfacecolor=self.options.pltcolor,
            color = self.options.pltcolor, 
            lw = self.options.width,
            alpha = self.options.opacity
        )
    
    def __copy__(self):
        return L0Point(self.coordinates[""])
    
    def pathify(self) -> Generator[Displayable, None, None]:
        yield self
        return
