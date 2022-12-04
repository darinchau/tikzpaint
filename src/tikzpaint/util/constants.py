import numpy as np
from numpy import pi as PI
from numpy import finfo
from numpy.typing import NDArray
from typing import TypeAlias

## Globally all the coordinates are only calculated to this precision
DECIMALS: int = 5

EPSILON = 10 ** - (DECIMALS + 1)
STRICT_EPSILON: float = finfo(float).eps # type: ignore

Number: TypeAlias = int | float | np.int64 | np.float64 | np.int32 | np.integer | np.floating
Coordinates: TypeAlias = tuple[Number, ...]
