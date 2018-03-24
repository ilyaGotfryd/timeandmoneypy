from decimal import *
""" 
 * Copyright (c) 2004 Domain Language, Inc. (http://domainlanguage.com) This
 * free software is distributed under the "MIT" licence. See file licence.txt.
 * For more information, see http://timeandmoney.sourceforge.net.
 
 * Ratio represents the unitless division of two quantities of the same type.
 * The key to its usefulness is that it defers the calculation of a decimal
 * value for the ratio. An object which has responsibility for the two values in
 * the ratio and understands their quantities can create the ratio, which can
 * then be used by any client in a unitless form, so that the client is not
 * required to understand the units of the quantity. At the same time, this
 * gives control of the precision and rounding rules to the client, when the
 * time comes to compute a decimal value for the ratio. The client typically has
 * the responsibilities that enable an appropriate choice of these parameters.
 """

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
