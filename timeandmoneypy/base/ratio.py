from decimal import *


class Ratio:
    def __init__(self, numerator, denominator):
        self._numerator = Decimal(numerator)
        self._denominator = Decimal(denominator)

    @staticmethod
    def of(numerator, denominator=1):
        #porting from Java, enforcing float type
        return Ratio(numerator, denominator)

    def decimal_value(self, scale, rounding_rule):
        precision_str = '0.{}1'.format(''if scale-1 == 0 else '0'*(scale-1))
        return (self._numerator / self._denominator).quantize(Decimal(precision_str), rounding=rounding_rule.value[1])

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Ratio):
            return self._numerator == other._numerator and self._denominator == other._denominator
        else:
            raise TypeError('Expected Ratio but presented {} type '.format(other.__class__))

    def times(self, multiplier):
        if isinstance(multiplier, Ratio):
            return Ratio(self._numerator * multiplier._numerator, self._denominator * multiplier._denominator)
        else:
            return Ratio(self._numerator * Decimal(multiplier), self._denominator)

    def __mul__(self, other):
        return self.times(other)

    def __str__(self):
        return "{}/{}".format(self._numerator, self._denominator)
