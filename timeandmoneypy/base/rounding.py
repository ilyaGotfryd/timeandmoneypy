from decimal import *
from enum import Enum


class Rounding(Enum):
    CEILING = (0, ROUND_CEILING)
    UP = (1, ROUND_UP)
    DOWN = (2, ROUND_DOWN)
    FLOOR = (3, ROUND_FLOOR)
    HALF_UP = (4, ROUND_HALF_UP)
    HALF_DOWN = (5, ROUND_HALF_DOWN)
    HALF_EVEN = (6, ROUND_HALF_EVEN)
    UNNECESSARY = (7, None)
