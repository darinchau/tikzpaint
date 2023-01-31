from tikzpaint.figures import Displayable
from tikzpaint.util import Coordinates, copy
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

class L0Curve(Displayable):
    """Implementation of a curve that can be drawn on the figure
    c1: starting point
    d1: control point for c1
    c2: ending point
    d2: control point for c2"""
    def __init__(self, c1: Coordinates, d1: Coordinates, c2: Coordinates, d2: Coordinates):
        pass
    
    def tikzify(self):
        pass

    def plot(self, ax: Axes):
        pass
    
    def __copy__(self):        
        pass
