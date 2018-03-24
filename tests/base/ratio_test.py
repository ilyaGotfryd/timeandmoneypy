from unittest import TestCase
from hamcrest import *

from decimal import *
from timeandmoneypy.base.ratio import Ratio, Rounding

class RatioTest(TestCase):
    def test_big_decimal_ratio(self):
        r3over2 = Ratio.of(Decimal(3), Decimal(2));
        result = r3over2.decimal_value(1, Rounding.UNNECESSARY);
        assert_that(1.5, equal_to(result));

        # Ratio r10over3 = Ratio.of(new BigDecimal(10), new BigDecimal(3));
        # result = r10over3.decimalValue(3, Rounding.DOWN);
        # assertEquals(new BigDecimal("3.333"), result);
        #
        # result = r10over3.decimalValue(3, Rounding.UP);
        # assertEquals(new BigDecimal("3.334"), result);
        #
        # Ratio rManyDigits = Ratio.of(new BigDecimal("9.001"), new BigDecimal(3));
        # result = rManyDigits.decimalValue(6, Rounding.UP);
        # assertEquals(new BigDecimal("3.000334"), result);
        #
        # result = rManyDigits.decimalValue(7, Rounding.UP);
        # assertEquals(new BigDecimal("3.0003334"), result);
        #
        # result = rManyDigits.decimalValue(7, Rounding.HALF_UP);
        # assertEquals(new BigDecimal("3.0003333"), result);