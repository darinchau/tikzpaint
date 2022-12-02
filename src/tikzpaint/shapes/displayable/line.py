from tikzpaint.figures import Displayable
import matplotlib.pyplot as plt

class L0Line(Displayable):
    """Implementation of a line that could be drawn on a figure"""
    name = "Line"
    def __init__(self, start: tuple, end: tuple):
        self.coordinates["start"] = start
        self.coordinates["end"] = end
    
    def tikzify(self):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        return f"\\draw[{self.tikz_options}] {start} -- {end};"
    
    def plot(self):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        x1, y1, x2, y2 = start[0], start[1], end[0] - start[0], end[1] - start[1]
        plt.arrow(x1, x2, y1, y2, head_width=0.01, head_length=0.03)
    
    def __copy__(self):
        return L0Line(self.coordinates["start"], self.coordinates["end"])