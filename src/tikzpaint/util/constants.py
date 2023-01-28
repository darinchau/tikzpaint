import numpy as np
from numpy import pi as PI
from numpy import finfo
from numpy.typing import NDArray
from typing import TypeAlias, TypeVar

## Globally all the coordinates are only calculated to this precision
DECIMALS: int = 5

EPSILON = 10 ** - (DECIMALS + 1)

# Strict epsilon is a private variable that we can only use with iszero
STRICT_EPSILON = 7./3-4./3-1
