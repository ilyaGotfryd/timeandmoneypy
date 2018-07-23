from unittest import TestCase
from hamcrest import *
from pytz import timezone
from timeandmoneypy.time.calendar_date import CalendarDate
from timeandmoneypy.time.time_point import TimePoint

class CalendarDateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feb17 = CalendarDate._from(2003, 2, 17)
        cls.mar13 = CalendarDate._from(2003, 3, 13)
        cls.gmt = timezone("GMT")
        cls.ct = timezone("America/Chicago")

    def test_comparison(self):
        assert_that(self.feb17.is_before(self.mar13), equal_to(True))
        assert_that(self.mar13.is_before(self.feb17), equal_to(False))
        assert_that(self.feb17.is_before(self.feb17), equal_to(False))
        assert_that(self.feb17.is_after(self.mar13), equal_to(False))
        assert_that(self.mar13.is_after(self.feb17), equal_to(True))
        assert_that(self.feb17.is_after(self.feb17), equal_to(False))

    def test_start_as_time_point(self):
        feb17_as_ct = self.feb17.start_as_time_point(self.ct)
        feb17_hour_0_ct = TimePoint.at_midnight(2003, 2, 17, self.ct)
        assert_that(feb17_hour_0_ct, equal_to(feb17_as_ct))

    # def test_as_time_interval(self):
    #     feb17_as_ct = self.feb17.as_time_interval(self.ct)
    #     feb17_hour0_ct = TimePoint.at_midnight(2003, 2, 17, self.ct)
    #     feb18_hour0_ct = TimePoint.at_midnight(2003, 2, 18, self.ct)
    #     assert_that("start", feb17_hour0_ct, feb17_as_ct.start())
    #     assert_that("end", feb18_hour0_ct, feb17_as_ct.end())
