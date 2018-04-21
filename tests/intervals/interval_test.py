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

    def test_open_interval(self):
        exRange = Interval.over(Decimal(-5.5), False, Decimal(6.6), True)
        assert_that(exRange.includes(Decimal(5.0)), equal_to(True))
        assert_that(exRange.includes(Decimal(-5.5)), equal_to(False))
        assert_that(exRange.includes(Decimal(-5.4999)), equal_to(True))
        assert_that(exRange.includes(Decimal(6.6)), equal_to(True))
        assert_that(exRange.includes(Decimal(6.601)), equal_to(False))
        assert_that(exRange.includes(Decimal(-5.501)), equal_to(False))

    def test_is_empty(self):
        assert_that(Interval.closed(5, 6).is_empty(), equal_to(False))
        assert_that(Interval.closed(6, 6).is_empty(), equal_to(False))
        assert_that(Interval.open(6, 6).is_empty(), equal_to(True))
        assert_that(self.c1_10c.empty_of_same_type().is_empty(), equal_to(True))

    def testIntersects(self):
        assert_that(self.c5_10c.intersects(self.c1_10c), equal_to(True), "c5_10c.intersects(c1_10c)")
        assert_that(self.c1_10c.intersects(self.c5_10c), equal_to(True), "c1_10c.intersectsself.(c5_10c)")
        assert_that(self.c4_6c.intersects(self.c1_10c), equal_to(True), "c4_6c.intersects(c1_10c)")
        assert_that(self.c1_10c.intersects(self.c4_6c), equal_to(True), "c1_10c.intersects(c4_6c)")
        assert_that(self.c5_10c.intersects(self.c5_15c), equal_to(True), "c5_10c.intersects(c5_15c)")
        assert_that(self.c5_15c.intersects(self.c1_10c), equal_to(True), "c5_15c.intersects(c1_10c)")
        assert_that(self.c1_10c.intersects(self.c5_15c), equal_to(True), "c1_10c.intersects(c5_15c)")
        assert_that(self.c1_10c.intersects(self.c12_16c), equal_to(False), "c1_10c.intersects(c12_16c)")
        assert_that(self.c12_16c.intersects(self.c1_10c), equal_to(False), "c12_16c.intersects(c1_10c)")
        assert_that(self.c5_10c.intersects(self.c5_10c), equal_to(True), "c5_10c.intersects(c5_10c)")
        assert_that(self.c1_10c.intersects(self.o10_12c), equal_to(False), "c1_10c.intersects(o10_12c)")
        assert_that(self.o10_12c.intersects(self.c1_10c), equal_to(False), "o10_12c.intersects(c1_10c)")

    def testIntersection(self):
        assert_that(self.c5_10c, equal_to(self.c5_10c.intersect(self.c1_10c)))
        assert_that(self.c5_10c, equal_to(self.c1_10c.intersect(self.c5_10c)))
        assert_that(self.c4_6c, equal_to(self.c4_6c.intersect(self.c1_10c)))
        assert_that(self.c4_6c, equal_to(self.c1_10c.intersect(self.c4_6c)))
        assert_that(self.c5_10c, equal_to(self.c5_10c.intersect(self.c5_15c)))
        assert_that(self.c5_10c, equal_to(self.c5_15c.intersect(self.c1_10c)))
        assert_that(self.c5_10c, equal_to(self.c1_10c.intersect(self.c5_15c)))
        assert_that(self.c1_10c.intersect(self.c12_16c).is_empty(), equal_to(True))
        assert_that(self.empty, equal_to(self.c1_10c.intersect(self.c12_16c)))
        assert_that(self.empty, equal_to(self.c12_16c.intersect(self.c1_10c)))
        assert_that(self.c5_10c, equal_to(self.c5_10c.intersect(self.c5_10c)))
        assert_that(self.empty, equal_to(self.c1_10c.intersect(self.o10_12c)))
        assert_that(self.empty, equal_to(self.o10_12c.intersect(self.c1_10c)))

    def test_greater_of_lower_limits(self):
        assert_that(Decimal(5), equal_to(self.c5_10c.greater_of_lower_limits(self.c1_10c)))
        assert_that(Decimal(5), equal_to(self.c1_10c.greater_of_lower_limits(self.c5_10c)))
        assert_that(Decimal(12), equal_to(self.c1_10c.greater_of_lower_limits(self.c12_16c)))
        assert_that(Decimal(12), equal_to(self.c12_16c.greater_of_lower_limits(self.c1_10c)))

    def test_lesser_of_upper_limits(self):
        assert_that(Decimal(10), equal_to(self.c5_10c.lesser_of_upper_limits(self.c1_10c)))
        assert_that(Decimal(10), equal_to(self.c1_10c.lesser_of_upper_limits(self.c5_10c)))
        assert_that(Decimal(6), equal_to(self.c4_6c.lesser_of_upper_limits(self.c12_16c)))
        assert_that(Decimal(6), equal_to(self.c12_16c.lesser_of_upper_limits(self.c4_6c)))

    def test_covers_interval(self):
        assert_that(self.c5_10c.covers(self.c1_10c), equal_to(False))
        assert_that(self.c1_10c.covers(self.c5_10c), equal_to(True))
        assert_that(self.c4_6c.covers(self.c1_10c), equal_to(False))
        assert_that(self.c1_10c.covers(self.c4_6c), equal_to(True))
        assert_that(self.c5_10c.covers(self.c5_10c), equal_to(True))
        half_open5_10 = Interval.over(Decimal(5), False, Decimal(10), True)
        assert_that(self.c5_10c.covers(half_open5_10), equal_to(True),"closed incl left-open")
        assert_that(half_open5_10.covers(half_open5_10), equal_to(True), "left-open incl left-open")
        assert_that(half_open5_10.covers(self.c5_10c), equal_to(False), "left-open doesn't include closed")
        half_closed5_10 = Interval.over(Decimal(5), True, Decimal(10), False)
        assert_that(self.c5_10c.covers(half_closed5_10), equal_to(True), "closed incl right-open")
        assert_that(half_closed5_10.covers(half_closed5_10), equal_to(True), "right-open incl right-open")
        assert_that(half_closed5_10.covers(self.c5_10c), equal_to(False), "right-open doesn't include closed")

    def test_gap(self):
        c1_3c = Interval.closed(1, 3)
        c5_7c = Interval.closed(5, 7)
        o3_5o = Interval.open(3, 5)
        c2_3o = Interval.over(2, True, 3, False)

        assert_that(o3_5o, equal_to(c1_3c.gap(c5_7c)))
        assert_that(c1_3c.gap(o3_5o).is_empty(), equal_to(True))
        assert_that(c1_3c.gap(c2_3o).is_empty(), equal_to(True))
        assert_that(c2_3o.gap(o3_5o).is_single_element(), equal_to(True))

    def test_relative_complement_disjoint(self):
        c1_3c = Interval.closed(1, 3)
        c5_7c = Interval.closed(5, 7)
        complement = c1_3c.complement_relative_to(c5_7c)
        assert_that(len(complement), equal_to(1))
        assert_that(complement[0], equal_to(c5_7c))

    def test_relative_complement_disjoint_adjacent_open(self):
        c1_3o = Interval.over(1, True, 3, False)
        c3_7c = Interval.closed(3, 7)
        complement = c1_3o.complement_relative_to(c3_7c)
        assert_that(len(complement), equal_to(1))
        assert_that(complement[0], equal_to(c3_7c))

    def test_relative_complement_overlap_left(self):
        c1_5c = Interval.closed(1, 5)
        c3_7c = Interval.closed(3, 7)
        complement = c3_7c.complement_relative_to(c1_5c)
        c1_3o = Interval.over(1, True, 3, False)
        assert_that(len(complement), equal_to(1))
        assert_that(complement[0], equal_to(c1_3o))

    def test_relative_complement_overlap_right(self):
        c1_5c = Interval.closed(1, 5)
        c3_7c = Interval.closed(3, 7)
        complement = c1_5c.complement_relative_to(c3_7c)
        o5_7c = Interval.over(5, False, 7, True)
        assert_that(len(complement), equal_to(1))
        assert_that(complement[0], equal_to(o5_7c))

    def test_relative_complement_adjacent_closed(self):
        c1_3c = Interval.closed(1, 3)
        c5_7c = Interval.closed(5, 7)
        complement = c1_3c.complement_relative_to(c5_7c)
        assert_that(len(complement), equal_to(1))
        assert_that(complement[0], equal_to(c5_7c))

    def test_relative_complement_enclosing(self):
        c3_5c = Interval.closed(3, 5)
        c1_7c = Interval.closed(1, 7)
        complement = c1_7c.complement_relative_to(c3_5c)
        assert_that(len(complement), equal_to(0))

    def test_relative_complement_equal(self):
        c1_7c = Interval.closed(1, 7)
        complement = c1_7c.complement_relative_to(c1_7c)
        assert_that(len(complement), equal_to(0))

    def test_relative_complement_enclosed(self):
        c3_5c = Interval.closed(3, 5)
        c1_7c = Interval.closed(1, 7)
        c1_3o = Interval.over(1, True, 3, False)
        o5_7c = Interval.over(5, False, 7, True)
        complement = c3_5c.complement_relative_to(c1_7c)
        assert_that(len(complement), equal_to(2))
        assert_that(complement[0], equal_to(c1_3o))
        assert_that(complement[1], equal_to(o5_7c))

    def test_relative_complement_enclosed_end_point(self):
        o3_5o = Interval.open(3, 5)
        c3_5c = Interval.closed(3, 5)
        complement = o3_5o.complement_relative_to(c3_5c)
        assert_that(len(complement), equal_to(2))
        assert_that(complement[0].includes(3), equal_to(True))

    def testIsSingleElement(self):
        assert_that(self.o1_1c.is_single_element(), equal_to(True))
        assert_that(self.c1_1c.is_single_element(), equal_to(True))
        assert_that(self.c1_1o.is_single_element(), equal_to(True))
        assert_that(self.c1_10c.is_single_element(), equal_to(False))
        assert_that(self.o1_1o.is_single_element(), equal_to(False))

    def test_equals_for_one_point_intervals(self):
        assert_that(self.o1_1c, equal_to(self.c1_1o))
        assert_that(self.o1_1c, equal_to(self.c1_1c))
        assert_that(self.c1_1o, equal_to(self.c1_1c))
        assert_that(self.o1_1c.equals(self.o1_1o), equal_to(False))

    def test_equals_for_empty_intervals(self):
        assert_that(self.c1_10c.empty_of_same_type(), equal_to(self.c4_6c.empty_of_same_type()))

    def test_relative_complement_enclosed_open(self):
        o3_5o = Interval.open(3, 5)
        c1_7c = Interval.closed(1, 7)
        c1_3c = Interval.closed(1, 3)
        c5_7c = Interval.closed(5, 7)
        complement = o3_5o.complement_relative_to(c1_7c)
        assert_that(len(complement), equal_to(2))
        assert_that(complement[0], equal_to(c1_3c))
        assert_that(complement[1], equal_to(c5_7c))
