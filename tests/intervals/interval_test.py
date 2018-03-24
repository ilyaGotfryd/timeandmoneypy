from unittest import TestCase
from hamcrest import *
from decimal import Decimal
from timeandmoneypy.intervals.interval import Interval


class IntervalTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty = Interval.open(Decimal(1), Decimal(1))
        cls.c5_10c = Interval.closed(Decimal(5), Decimal(10))
        cls.c1_10c = Interval.closed(Decimal(1),  Decimal(10))
        cls.c4_6c = Interval.closed(Decimal(4), Decimal(6))
        cls.c5_15c = Interval.closed(Decimal(5),  Decimal(15))
        cls.c12_16c = Interval.closed(Decimal(12), Decimal(16))
        cls.o10_12c = Interval.over(Decimal(10), False, Decimal(12), True)
        cls.o1_1c = Interval.over(Decimal(1), False, Decimal(1), True)
        cls.c1_1o = Interval.over(Decimal(1), True, Decimal(1), False)
        cls.c1_1c = Interval.over(Decimal(1), True, Decimal(1), True)
        cls.o1_1o = Interval.over(Decimal(1), False,  Decimal(1), False)

    def testAbstractCreation(self):
        concrete = Interval(1, True, 3, True)
        new_interval = concrete.new_of_same_type(1, False, 4, False)

        expected = Interval(1, False, 4, False)
        assert_that(new_interval, equal_to(expected))

    def test_is_below(self):
        range = Interval.closed(Decimal(-5.5), Decimal(6.6))
        assert_that(range.is_below(Decimal(5.0)), equal_to(False))
        assert_that(range.is_below(Decimal(-5.5)), equal_to(False))
        assert_that(range.is_below(Decimal(-5.4999)), equal_to(False))
        assert_that(range.is_below(Decimal(6.6)), equal_to(False))
        assert_that(range.is_below(Decimal(6.601)), equal_to(True))
        assert_that(range.is_below(Decimal(-5.501)), equal_to(False))

    def testIncludes(self):
        range = Interval.closed(Decimal(-5.5), Decimal(6.6))
        assert_that(range.includes(Decimal(5.0)), equal_to(True))
        assert_that(range.includes(Decimal(-5.5)), equal_to(True))
        assert_that(range.includes(Decimal(-5.4999)), equal_to(True))
        assert_that(range.includes(Decimal(6.6)), equal_to(True))
        assert_that(range.includes(Decimal(6.601)), equal_to(False))
        assert_that(range.includes(Decimal(-5.501)), equal_to(False))
