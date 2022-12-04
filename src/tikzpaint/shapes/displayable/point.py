from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from typing import Any

class L0Point(Displayable):
    """Implementation of a point that could be drawn on a figure"""
    def __init__(self, p: Coordinates):
        self.coordinates[""] = copy(p)
    
    def tikzify(self):
        p = self.coordinates[""]
        return f"\\node[{self.tikz_options}] at {p} {{}}"

    def plot(self):
        x, y = self.coordinates[""]
        plt.plot(x, y, 
            marker="o", 
            markersize=self.options.width * 10, 
            markeredgecolor=self.options.pltcolor, 
            markerfacecolor=self.options.pltcolor
        )
    
    def __copy__(self):
        return L0Point(self.coordinates[""])