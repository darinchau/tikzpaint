from tikzpaint.figures import Displayable
import matplotlib.pyplot as plt

class L0Arrow(Displayable):
    """Implementation of an arrow that could be drawn on a figure"""
    name = "Arrow"
    def __init__(self, start: tuple, end: tuple):
        self.coordinates["start"] = start
        self.coordinates["end"] = end
    
    def tikzify(self, options: str):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        if not options:
            return f"\\draw[->] {start} -- {end};"
        else:
            return f"\\draw[{options}, ->] {start} -- {end};"

    def plot(self):
        start = self.coordinates["start"]
        end = self.coordinates["end"]
        xcoords, ycoords = (start[0], end[0]), (start[1], end[1])
        plt.plot(xcoords, ycoords)
    
    def __copy__(self):
        return L0Arrow(self.coordinates["start"], self.coordinates["end"])