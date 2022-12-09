from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Iterable

class L0Path(Displayable):
    """Implementation of a path that could be drawn on a figure"""
    def __init__(self, coords: list[Coordinates]) -> None:
        for i, t in enumerate(coords):
            self.coordinates[i] = copy(t)
        self.lencoords = len(coords)
    
    def plot(self, ax: Axes):
        x, y = [], []
        for i in range(self.lencoords):
            _x, _y = self.coordinates[i]
            x.append(_x)
            y.append(_y)

        ax.plot(x, y, ls = "-", 
            color = self.options.pltcolor, 
            lw = self.options.width,
            alpha = self.options.opacity
        )

    def tikzify(self) -> str:
        coords = " -- ".join([str(self.coordinates[i]) for i in range(self.lencoords)])
        return f"\\draw[{self.tikz_options}] {coords};"
    
    def __copy__(self):
        return L0Path([self.coordinates[i] for i in range(self.lencoords)])