from unittest import TestCase
from hamcrest import *
from decimal import Decimal
from timeandmoneypy.intervals.interval import Interval
from timeandmoneypy.intervals.interval_sequence import IntervalSequence

class IntervalSequenceTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c5_10c = Interval.closed(Decimal(5), Decimal(10))
        cls.o10_12c = Interval.over(Decimal(10), False, Decimal(12), True)
        cls.o11_20c = Interval.over(Decimal(11), False, Decimal(20), True)
        cls.o12_20o = Interval.over(Decimal(12), False, Decimal(20), False)
        cls.c20_25c = Interval.closed(Decimal(20), Decimal(25))
        cls.o25_30c = Interval.over(Decimal(25), False, Decimal(30), True)
        cls.o30_35o = Interval.over(Decimal(30), False, Decimal(35), False)

    def test_iterate(self):
        interval_sequence = IntervalSequence()
        assert_that(interval_sequence.is_empty(), equal_to(True))
        interval_sequence.add(self.c5_10c)
        interval_sequence.add(self.o10_12c)
        count = 0
        for interval in interval_sequence:
            count += 1
            if count == 1:
                assert_that(interval, equal_to(self.c5_10c))
            if count == 2:
                assert_that(interval), equal_to(self.o10_12c)
        assert_that(count, equal_to(2))

    def test_insert_out_of_order(self):
        interval_sequence = IntervalSequence()
        assert_that(interval_sequence.is_empty(), equal_to(True))
        interval_sequence.add(self.o10_12c)
        interval_sequence.add(self.c5_10c)
        count = 0
        for interval in interval_sequence:
            count += 1
            if count == 1:
                assert_that(interval, equal_to(self.c5_10c))
            if count == 2:
                assert_that(interval), equal_to(self.o10_12c)
        assert_that(count, equal_to(2))

    def test_gaps(self):
        interval_sequence = IntervalSequence()
        interval_sequence.add(self.c5_10c)
        interval_sequence.add(self.o10_12c)
        interval_sequence.add(self.c20_25c)
        interval_sequence.add(self.o30_35o)
        gaps = interval_sequence.gaps()
        count = 0
        for gap in gaps:
            count+=1
            if count == 1:
                assert_that(gap, equal_to(self.o12_20o))
            if count == 2:
                assert_that(gap, equal_to(self.o25_30c))
        assert_that(count, equal_to(2))

    def test_overlapping(self):
        interval_sequence = IntervalSequence()
        interval_sequence.add(self.o10_12c)
        interval_sequence.add(self.o11_20c)
        count = 0
        for interval in interval_sequence:
            count += 1
            if count == 1:
                assert_that(interval, equal_to(self.o10_12c))
            if count == 2:
                assert_that(interval), equal_to(self.o11_20c)
        assert_that(count, equal_to(2))

    def test_extent(self):
        interval_sequence = IntervalSequence()
        interval_sequence.add(self.c5_10c)
        interval_sequence.add(self.o10_12c)
        interval_sequence.add(self.c20_25c)
        assert_that(Interval.closed(5, 25), interval_sequence.extent())