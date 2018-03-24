from decimal import *
from enum import Enum

class Rounding(Enum):
    UNNECESSARY = (0, None)
    DOWN = (1, ROUND_DOWN)
    UP = (2, ROUND_UP)
    HALF_DOWN = (3, ROUND_HALF_DOWN)
    HALF_UP = (4, ROUND_HALF_UP)

class Ratio:
    def __init__(self, numerator, denominator):
        self._numerator = Decimal(numerator)
        self._denominator = Decimal(denominator)

    @staticmethod
    def of(numerator, denominator=1):
        #porting from Java, enforcing float type
        return Ratio(numerator, denominator)

    def decimal_value(self, scale, rounding_rule):
        return self._numerator / self._denominator

