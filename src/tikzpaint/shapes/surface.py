from typing import Callable, Generator, Any
import matplotlib.pyplot as plt
from abc import abstractmethod as virtual

from tikzpaint.util import copy, isZero, num_parameters
from tikzpaint.figures import Drawable, Displayable 
from tikzpaint.util import Coordinates

from tikzpaint.shapes.displayable.path import L0Path

class ParametricSurface(Drawable):
    """Implementation of an n-dimensional surface (n-1 manifold) drawn on a figure
    f: function that takes in n-1 parameters and returns coordinates n
    iter_list is the sample points you want to use"""
    def __init__(self, f: Callable[..., Coordinates], *iters: Generator[float, None, None]):
        if type(self) == ParametricSurface:
            raise TypeError("Cannot instantiate parametric surface directly")
        
        self.num_params = self.get_num_params()
        
        if self.num_params != num_parameters(f):
            raise ValueError(f"The number of parameters in the function ()")

        if self.num_params != len(iters):
            raise ValueError(f"The number of dimensions does not match number of iterators {len(iters)}")

        self.ranges: list[list[float]] = [list(it) for it in iters]

        input1 = [r[0] for r in self.ranges]
        self.n = len(f(*input1))

        self.f = f
    
    @virtual
    def get_num_params(self) -> int:
        """Returns the number of parameters from the surface. Aka this number is the n in n-manifold"""
        pass

    @virtual
    def gen_path(self, f: Callable) -> Generator[Displayable, None, None]:
        pass
    
    def draw(self) -> Generator[Displayable, None, None]:
        for d in self.gen_path(self.f):
            yield d

class Surface1D(ParametricSurface):
    """An implementation of the 1 manifold
    f: function that takes in n-1 parameters and returns coordinates n
    iter_list is the sample points you want to use"""
    def get_num_params(self):
        return 1

    def gen_path(self, f) -> Generator[Displayable, None, None]:
        it = self.ranges[0]
        coords = [f(it[i]) for i in range(len(it) - 1)]
        yield L0Path(coords)
    

# class Surface2D(ParametricSurface):
#     """An implementation of the 2 manifold
#     f: function that takes in n-1 parameters and returns coordinates n
#     iter_list is the sample points you want to use"""
#     def get_num_params(self) -> int:
#         return 2
    
#     def gen_path(self, f: Callable) -> Generator[Displayable, None, None]:
#         it1, it2 = self.ranges
#         for i in range(len(it1) - 1):
#             for j in range(len(it2) - 1):
#                 yield L0Line(f(it1[i], it2[j]), f(it1[i + 1], it2[j]))
#                 yield L0Line(f(it1[i], it2[j]), f(it1[i], it2[j + 1]))

# class Surface3D(ParametricSurface):
#     """An implementation of the 3 manifold
#     f: function that takes in n-1 parameters and returns coordinates n
#     iter_list is the sample points you want to use"""
#     def get_num_params(self) -> int:
#         return 3
    
#     def gen_path(self, f: Callable) -> Generator[Displayable, None, None]:
#         it1, it2, it3 = self.ranges
#         for i in range(len(it1) - 1):
#             for j in range(len(it2) - 1):
#                 for k in range(len(it3) - 1):
#                     # Coordinates
#                     llb = f(it1[i], it2[j], it3[k])
#                     llf = f(it1[i], it2[j], it3[k + 1])
#                     lub = f(it1[i], it2[j + 1], it3[k])
#                     rlb = f(it1[i + 1], it2[j], it3[k])

#                     yield L0Line(llb, rlb)
#                     yield L0Line(llb, lub)
#                     yield L0Line(llb, llf)