from unittest import TestCase
from hamcrest import *
from decimal import Decimal
from timeandmoneypy.intervals.interval import Interval
from timeandmoneypy.intervals.linear_interval_map import LinearIntervalMap

class IntervalMapTest(TestCase):

    def test_lookup(self):
        map = LinearIntervalMap()
        map.put(Interval.closed(1, 3), "one-three")
        map.put(Interval.closed(5, 9), "five-nine")
        map.put(Interval.open(9, 12), "ten-eleven")

        assert_that(map.contains_key(0), equal_to(False))
        assert_that(map.contains_key(1), equal_to(True))
        assert_that(map.contains_key(2), equal_to(True))
        assert_that(map.contains_key(3), equal_to(True))
        assert_that(map.contains_key(4), equal_to(False))
        assert_that(map.contains_key(5), equal_to(True))
        assert_that(map.contains_key(9), equal_to(True))
        assert_that(map.contains_key(11), equal_to(True))
        assert_that(map.contains_key(12), equal_to(False))
        assert_that(map.contains_key(13), equal_to(False))
        assert_that(map.contains_key(None), equal_to(False))

        assert_that(map.get(0), equal_to(None))
        assert_that(map.get(1), equal_to("one-three"))
        assert_that(map.get(2), equal_to("one-three"))
        assert_that(map.get(3), equal_to("one-three"))
        assert_that(map.get(4), equal_to(None))
        assert_that(map.get(5), equal_to("five-nine"))
        assert_that(map.get(9), equal_to("five-nine"))
        assert_that(map.get(10), equal_to("ten-eleven"))
        assert_that(map.get(11), equal_to("ten-eleven"))
        assert_that(map.get(12), equal_to(None))
        assert_that(map.get(13), equal_to(None))
        assert_that(map.get(None), equal_to(None))

    def test_remove(self):
        map = LinearIntervalMap();
        map.put(Interval.closed(1, 10), "one-ten")
        map.remove(Interval.closed(3, 5))
        assert_that(map.get(2), equal_to("one-ten"))
        assert_that(map.get(3), equal_to(None))
        assert_that(map.get(4), equal_to(None))
        assert_that(map.get(5), equal_to(None))
        assert_that(map.get(6), equal_to("one-ten"))

    def test_construction_overwrite_overlap(self):
        map = LinearIntervalMap()
        map.put(Interval.closed(1, 2), "one-three")
        map.put(Interval.closed(5, 9), "five-nine")
        map.put(Interval.open(9, 12), "ten-eleven")
        assert_that(map.get(10), equal_to("ten-eleven"))
        assert_that(map.get(11), equal_to("ten-eleven"))
        assert_that(map.get(12), equal_to(None))

        eleven_thirteen = Interval.closed(11, 13)
        assert_that(map.contains_intersecting_key(eleven_thirteen), equal_to(True))
        map.put(eleven_thirteen, "eleven-thirteen");
        assert_that(map.get(10), equal_to("ten-eleven"))
        assert_that(map.get(11), equal_to("eleven-thirteen"))
        assert_that(map.get(12), equal_to("eleven-thirteen"))

    def test_construction_overwrite_middle(self):
        map = LinearIntervalMap()
        map.put(Interval.closed(1,3), "one-three")
        map.put(Interval.closed(5, 9), "five-nine")
        map.put(Interval.open(9, 12), "ten-eleven")
        assert_that(map.get(6), equal_to("five-nine"))
        assert_that(map.get(7), equal_to("five-nine"))
        assert_that(map.get(8), equal_to("five-nine"))
        assert_that(map.get(9), equal_to("five-nine"))

        seven_eight = Interval.closed(7, 8)
        assert_that(map.contains_intersecting_key(seven_eight), equal_to(True))
        map.put(seven_eight, "seven-eight")
        assert_that(map.get(6), equal_to("five-nine"))
        assert_that(map.get(7), equal_to("seven-eight"))
        assert_that(map.get(8), equal_to("seven-eight"))
        assert_that(map.get(9), equal_to("five-nine"))

    def test_construction_overwrite_multiple(self):
        map = LinearIntervalMap()
        map.put(Interval.closed(1, 2), "one-two")
        map.put(Interval.closed(3, 4), "three-four")
        map.put(Interval.closed(5, 6), "five-six")
        map.put(Interval.closed(8, 9), "eight-nine")
        map.put(Interval.closed(3, 8), "three-eight")
        assert_that(map.get(2), equal_to("one-two"))
        assert_that(map.get(3), equal_to("three-eight"))
        assert_that(map.get(4), equal_to("three-eight"))
        assert_that(map.get(5), equal_to("three-eight"))
        assert_that(map.get(6), equal_to("three-eight"))
        assert_that(map.get(7), equal_to("three-eight"))
        assert_that(map.get(8), equal_to("three-eight"))
        assert_that(map.get(9), equal_to("eight-nine"))
