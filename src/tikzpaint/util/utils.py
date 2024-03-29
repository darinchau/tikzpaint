import numpy as np
from typing import Any, Callable, Type, TypeVar
from abc import ABC
from abc import abstractmethod as virtual
from functools import wraps
from functools import total_ordering, cache
from inspect import signature

from tikzpaint.util.constants import NDArray, EPSILON, STRICT_EPSILON

def isZero(obj: Any, strict: bool = False) -> bool:
    """Returns true if a is not zero, false otherwise. Automatically handles floating point comparison. 
    Strict flag is true, then the number must be 0. 
    For types that are not number, resort to the __bool__ method and return not(a)"""
    epsilon: float = STRICT_EPSILON if strict else EPSILON #type: ignore
    try:
        if isinstance(obj, np.ndarray):
            # Not not is same as bool()
            return not not np.all(np.abs(obj) < epsilon)
        else:
            return np.abs(obj) < epsilon
    except TypeError:
        if "__iszero__" not in dir(obj):
            raise TypeError(f"Object of type {type(obj).__name__} is not copyable!")
        return obj.__iszero__() #type: ignore

def isInteger(a: Any) -> bool:
    """Return true if a is (sufficiently close to) an integer"""
    if "__isint__" in dir(a):
        return a.__isint__() #type: ignore
    return isZero(a % 1, strict = True)

def isNumber(a: Any):
    """Returns true if a is a number. A custom class is a number if __iszero__ and __isint__ are both implemented"""
    if np.issubdtype(type(a), np.integer):
        return True
    
    if np.issubdtype(type(a), np.floating):
        return True
    
    if "__isint__" in dir(a) and "__iszero__" in dir(a):
        return True
    return False

_copyable = TypeVar("_copyable")
def copy(obj: _copyable) -> _copyable:
    """Makes a deep copy via the dunder copy method in a class. If the parameter is a list, returns the recursive deep copy"""
    if isinstance(obj, int | float | str):
        return obj
    
    if isinstance(obj, list):
        return [copy(x) for x in obj] #type: ignore
    
    if isinstance(obj, tuple):
        return tuple(copy(x) for x in obj) #type: ignore
    
    if isinstance(obj, dict):
        return {copy(k): copy(v) for k, v in obj.items()} #type: ignore
    
    if isinstance(obj, np.ndarray):
        return np.array(obj, dtype = obj.dtype)
    
    if "__copy__" in dir(obj) and "options" in dir(obj):
        newobj = obj.__copy__() #type: ignore
        newobj._options = copy(obj.options) #type: ignore
        return newobj
    
    if "__copy__" in dir(obj):
        return obj.__copy__() #type: ignore
    
    raise TypeError(f"Object of type {type(obj).__name__} is not copyable!")


def num_parameters(f: Callable):
    """Returns the number of parameters in the callable f"""
    return len(signature(f).parameters)

def to_superscript(a: int):
    SUPERSCRIPTS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
    st = "" if a >= 0 else "⁻"
    return st + "".join([SUPERSCRIPTS[int(i)] for i in str(abs(a))])
    
def to_subscript(a: int):
    SUBSCRIPTS = "₀₁₂₃₄₅₆₇₈₉"
    st = "" if a >= 0 else "₋"
    return st + "".join([SUBSCRIPTS[int(i)] for i in str(abs(a))])

def notFalse(kwargs: dict[Any, Any], kw: Any):
    return not kw in kwargs or kwargs[kw]

def domain(start: float, end: float, res: int, include_end: bool = False):
    r = res + 1 if include_end else res
    for i in range(r):
        yield start * i / res + end * (1 - i / res)
    return