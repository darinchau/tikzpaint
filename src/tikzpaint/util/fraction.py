from __future__ import annotations
from math import gcd

class Fraction:
    """Helper class to store a fraction to maintain precision and hide all the cleaning and stuff. Returns a/b in the constructor if a or b is a fraction"""
    __slots__ = '__val'
    def __init__(self, a: int | Fraction = 0, b: int | Fraction= 1) -> None:
        if b == 0:
            raise ValueError("Divide by 0!")
        
        if (not isinstance(a, int)) and (not isinstance(a, Fraction)):
            raise TypeError(f"{a=} is not an integer/Fraction but type {type(a).__name__}")

        if (not isinstance(b, int)) and (not isinstance(b, Fraction)):
            raise TypeError(f"{b=} is not an integer/Fraction but type {type(b).__name__}")

        x: int = 1
        y: int = 1

        if isinstance(a, Fraction):
            x *= a.numerator
            y *= a.denominator
        else:
            x *= a
        
        if isinstance(b, Fraction):
            x *= b.denominator
            y *= b.numerator
        else:
            y *= b

        self.__val: tuple[int, int] = (x, y)
        self.clean()
    
    @property
    def numerator(self):
        return self.__val[0]
    
    @property
    def denominator(self):
        return self.__val[1]
    
    def clean(self):
        """Simplify and put the negative sign on top"""
        a, b = self.__val
        factor = gcd(abs(a), abs(b))
        newa: int
        newb: int
        if b > 0:
            newa, newb = a // factor, b // factor
        else:
            newa, newb = -a // factor, -b // factor
        self.__val = (newa, newb)
        return self
    
    def __add__(self, other: int | Fraction):
        a, b = self.__val
        if isinstance(other, int):
            other = Fraction(other)
        c, d = other.__val
        return Fraction(a * d + b * c, b * d)
    
    def __iadd__(self, other: int | Fraction):
        if isinstance(other, int):
            other = Fraction(other)
        a, b = self.__val
        c, d = other.__val
        self.__val = (a * d + b * c, b * d)
        return self.clean()
    
    def __mul__(self, other: int | Fraction):
        a, b = self.__val
        if isinstance(other, int):
            other = Fraction(other)
        c, d = other.__val
        return Fraction(a * c, b * d)
    
    def __neg__(self):
        a, b = self.__val
        return Fraction(-a, b)
    
    def __truediv__(self, other: int | Fraction):
        a, b = self.__val
        if isinstance(other, int):
            other = Fraction(other)
        c, d = other.__val
        return Fraction(a * d, b * c)
    
    def __sub__(self, other: int | Fraction):
        a, b = self.__val
        if isinstance(other, int):
            other = Fraction(other)
        c, d = other.__val
        return Fraction(a * d - b * c, b * d)
    
    def __le__(self, other) -> bool:
        a, b = self.__val
        if not isinstance(other, Fraction):
            return a/b <= other
        c, d = other.__val
        return a * d < b * c
    
    def __eq__(self, other) -> bool:
        a, b = self.clean().__val
        if not isinstance(other, Fraction):
            return a/b == other
        c, d = other.clean().__val
        return a == c and b == d
    
    def __ne__(self, other) -> bool:
        return not(self == other)
    
    def __hash__(self):
        return hash(self.clean().__val)
    
    def __repr__(self) -> str:
        try:
            return str(int(self))
        except ValueError:
            return f"{self.__val[0]}/{self.__val[1]}"
    
    def __copy__(self):
        a, b = self.__val
        return Fraction(a, b)
    
    def __iter__(self):
        self.clean()
        yield self.__val[0]
        yield self.__val[1]
        return # Raise stopiteration
    
    def __int__(self) -> int:
        a, b = self.__val
        if gcd(a, b) == b:
            return int(a // b)
        raise ValueError(f"The fraction {self.__val[0]}/{self.__val[1]} is not an integer")
    
    def __float__(self) -> float:
        a, b = self.__val
        return a/b
    
    def __iszero__(self) -> bool:
        return self.__val[0] == 0
    
    def __isint__(self) -> bool:
        a, b = self.__val
        return gcd(a, b) == b