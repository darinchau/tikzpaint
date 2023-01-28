from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class L0Arrow(Displayable):
    """Implementation of an arrow that could be drawn on a figure. Note: arrows must be straight and they are not
    reall compatible with stereographic projections
    
    start: coordinates of the start of an arrow
    end: coordinates of the end of an arrow"""
    def __init__(self, start: Coordinates, end: Coordinates):
        self.coordinates["start"] = copy(start)
        self.coordinates["end"] = copy(end)
    
    def tikzify(self):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        if not self.tikz_options:
            return f"\\draw[->] {start} -- {end};"
        else:
            return f"\\draw[{self.tikz_options}, ->] {start} -- {end};"

    def plot(self, ax: Axes):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        x, y = start[0], start[1]
        dx, dy = end[0] - start[0], end[1] - start[1]
        ax.arrow(x, y, dx, dy, 
            color = self.options.pltcolor, 
            lw = self.options.width,
            alpha = self.options.opacity
        )
    
    def __copy__(self):        
        return L0Arrow(self.coordinates["start"], self.coordinates["end"])