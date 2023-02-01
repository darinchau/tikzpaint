from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class L0Curve(Displayable):
    """Implementation of a Bezier curve that can be drawn on the figure
    c1: starting point
    d1: control point for c1
    c2: ending point
    d2: control point for c2"""
    def __init__(self, c1: Coordinates, d1: Coordinates, c2: Coordinates, d2: Coordinates):
        self.coordinates["c1"] = c1
        self.coordinates["c2"] = c2
        self.coordinates["d1"] = d1
        self.coordinates["d2"] = d2
    
    def tikzify(self):
        c1 = self.coordinates["c1"]
        c2 = self.coordinates["c2"]
        d1 = self.coordinates["d1"]
        d2 = self.coordinates["d2"]
        return f"\\draw {c1} .. controls {d1} and {d2} .. {c2};"

    def plot(self, ax: Axes):
        raise NotImplementedError
    
    def __copy__(self):
        c1 = self.coordinates["c1"]
        c2 = self.coordinates["c2"]
        d1 = self.coordinates["d1"]
        d2 = self.coordinates["d2"]    
        return L0Curve(c1, d1, c2, d2)

    def pathify(self):
        raise NotImplementedError
    