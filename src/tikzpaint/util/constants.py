import numpy as np
from numpy import pi as PI
from numpy import finfo
from numpy.typing import NDArray
from typing import TypeAlias, TypeVar

## Globally all the coordinates are only calculated to this precision
DECIMALS: int = 5

EPSILON = 10 ** - (DECIMALS + 1)
STRICT_EPSILON: float = finfo(float).eps # type: ignore
