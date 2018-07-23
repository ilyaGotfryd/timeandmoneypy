from unittest import TestCase
from hamcrest import *

from decimal import *
from timeandmoneypy.base.ratio import Ratio
from timeandmoneypy.base.rounding import Rounding

class RatioTest(TestCase):
    def test_big_decimal_ratio(self):
        r3over2 = Ratio.of(Decimal(3), Decimal(2))
        result = r3over2.decimal_value(1, Rounding.UNNECESSARY)
        assert_that(result, equal_to(Decimal('1.5')))

        r10over3 = Ratio.of(Decimal(10), Decimal(3))
        result = r10over3.decimal_value(3, Rounding.DOWN)
        assert_that(result, equal_to(Decimal("3.333")))

        result = r10over3.decimal_value(3, Rounding.UP)
        assert_that(result, equal_to(Decimal("3.334")))

        rManyDigits = Ratio.of(Decimal("9.001"), Decimal(3))
        result = rManyDigits.decimal_value(6, Rounding.UP)
        assert_that(result, equal_to(Decimal("3.000334")))

        result = rManyDigits.decimal_value(7, Rounding.UP)
        assert_that(result, equal_to(Decimal("3.0003334")))

        result = rManyDigits.decimal_value(7, Rounding.HALF_UP)
        assert_that(result, Decimal("3.0003333"))

    def test_long_ratio(self):
        rManyDigits = Ratio.of(9001, 3000)
        result = rManyDigits.decimal_value(6, Rounding.UP)
        assert_that(result, equal_to(Decimal("3.000334")))

    def test_equals(self):
        assert_that(Ratio.of(100, 200), equal_to(Ratio.of(100, 200)))
        assert_that(Ratio.of(100, 200), equal_to(Ratio.of(Decimal("100"), Decimal("200"))))

    def test_multiply_numerator(self):
        rManyDigits = Ratio.of(9001, 3000)
        product = rManyDigits.times(Decimal("1.1"))
        assert_that(product, equal_to(Ratio.of(Decimal("9901.1"),  Decimal(3000))))

    def test_multiply_by_ratio(self):
        rManyDigits = Ratio.of(9001, 3000)
        product = rManyDigits * Ratio(5, 7)
        assert_that(product, equal_to(Ratio.of(9001*5, 3000*7)))

    def test_to_string(self):
        stringable_ratio = Ratio.of(Decimal('123.456'),Decimal('456.789'))
        assert_that("{}".format(stringable_ratio), equal_to("123.456/456.789"))
