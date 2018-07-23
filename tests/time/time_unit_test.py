from unittest import TestCase
from hamcrest import *
from pytz import timezone
from timeandmoneypy.time.time_unit import TimeUnit


class TimeUnitTest(TestCase):

    def test_to_string(self):
        assert_that(str(TimeUnit.month), equal_to("month"))

    def test_convertable_to_milliseconds(self):
        assert_that(TimeUnit.millisecond.is_convertible_to_milliseconds(), equal_to(True))
        assert_that(TimeUnit.hour.is_convertible_to_milliseconds(), equal_to(True))
        assert_that(TimeUnit.day.is_convertible_to_milliseconds(), equal_to(True))
        assert_that(TimeUnit.week.is_convertible_to_milliseconds(), equal_to(True))
        assert_that(TimeUnit.month.is_convertible_to_milliseconds(), equal_to(False))
        assert_that(TimeUnit.year.is_convertible_to_milliseconds(), equal_to(False))

    def test_comparison(self):
        assert_that(TimeUnit.hour.compare_to(TimeUnit.hour), equal_to(0))
        assert_that(TimeUnit.hour > TimeUnit.millisecond, equal_to(True))
        assert_that(TimeUnit.millisecond < TimeUnit.hour, equal_to(True))
        assert_that(TimeUnit.day > TimeUnit.hour, equal_to(True))
        assert_that(TimeUnit.hour < TimeUnit.day, equal_to(True))

        assert_that(TimeUnit.month > TimeUnit.day, equal_to(True))
        assert_that(TimeUnit.day < TimeUnit.month, equal_to(True))
        assert_that(TimeUnit.quarter > TimeUnit.hour, equal_to(True))

        assert_that(TimeUnit.month == TimeUnit.month, equal_to(True))
        assert_that(TimeUnit.quarter < TimeUnit.year, equal_to(True))
        assert_that(TimeUnit.year > TimeUnit.quarter, equal_to(True))

    def test_is_convertable_to(self):
        assert_that(TimeUnit.hour.is_convertible_to(TimeUnit.minute), equal_to(True))
        assert_that(TimeUnit.minute.is_convertible_to(TimeUnit.hour), equal_to(True))
        assert_that(TimeUnit.year.is_convertible_to(TimeUnit.month), equal_to(True))
        assert_that(TimeUnit.month.is_convertible_to(TimeUnit.year), equal_to(True))
        assert_that(TimeUnit.month.is_convertible_to(TimeUnit.hour), equal_to(False))
        assert_that(TimeUnit.hour.is_convertible_to(TimeUnit.month), equal_to(False))

    def test_next_finer_unit(self):
        assert_that(TimeUnit.hour.next_finer_unit(), equal_to(TimeUnit.minute))
        assert_that(TimeUnit.quarter.next_finer_unit(), equal_to(TimeUnit.month))
