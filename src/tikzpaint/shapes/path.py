from tikzpaint.figures import Displayable
import matplotlib.pyplot as plt

class Path(Displayable):
    """Implementation of a path that could be drawn on a figure"""
    name = "Path"
    def __init__(self, coords: list[tuple]) -> None:
        for i, t in enumerate(coords):
            self.coordinates[i] = t
        self.lencoords = len(coords)
    
    def plot(self):
        x, y = [], []
        for i in range(self.lencoords):
            _x, _y = self.coordinates[i]
            x.append(_x)
            y.append(_y)
        plt.plot(x, y, "-k")

    def tikzify(self, options: str) -> str:
        coords = " -- ".join([str(self.coordinates[i]) for i in range(self.lencoords)])
        return f"\\draw[{options}] {coords};"
    
    def __copy__(self):
        return Path([self.coordinates[i] for i in range(self.lencoords)])