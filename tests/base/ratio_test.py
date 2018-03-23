from unittest import TestCase
from hamcrest import *

class RatioTest(TestCase):
    def test_big_decimal_ratio() {
        Ratio r3over2 = Ratio.of(new BigDecimal(3), new BigDecimal(2));
        BigDecimal result = r3over2.decimalValue(1, Rounding.UNNECESSARY);
        assertEquals(new BigDecimal("1.5"), result);

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
    }