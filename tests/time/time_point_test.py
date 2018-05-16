from unittest import TestCase
from hamcrest import *
from pytz import timezone
from timeandmoneypy.time.time_point import TimePoint

class TimePointTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.AM = "AM"
        cls.PM = "PM"

        cls.gmt = timezone("GMT")
        cls.pt = timezone("America/Los_Angeles")
        cls.ct = timezone("America/Chicago")

        cls.dec19_2003 = TimePoint.at_midnight_GMT(2003, 12, 19)
        cls.dec20_2003 = TimePoint.at_midnight_GMT(2003, 12, 20)
        cls.dec21_2003 = TimePoint.at_midnight_GMT(2003, 12, 21)
        cls.dec22_2003 = TimePoint.at_midnight_GMT(2003, 12, 22)

    def test_creation_with_default_timezone(self):
        expected = TimePoint.at_GMT(2004, 1, 1, 0, 0, 0, 0)
        assert_that(TimePoint.at_midnight_GMT(2004, 1, 1), equal_to(expected), "at midnight")
        assert_that(TimePoint.at_GMT(2004, 1, 1, 0, 0), equal_to(expected), "hours in 24hr clock")
        assert_that(TimePoint.at_12_hr(2004, 1, 1, 12, self.AM, 0, 0, 0, self.gmt), equal_to(expected),
                    "hours in 12hr clock")
        assert_that(TimePoint.parse_GMT_from("2004/1/1", "%Y/%m/%d"), equal_to(expected),
                    "date from formatted String")
        assert_that(TimePoint.at_12_hr(2004, 1, 1, 12, self.PM, 0, 0, 0, self.gmt),
                    equal_to(TimePoint.at_GMT(2004, 1, 1, 12, 0)), "pm hours in 12hr clock")

    def test_creation_with_time_zone(self):
        #   TimePoints are based on miliseconds from the Epoc. They do not have a
        #   "timezone". When that basic value needs to be converted to or from a
        #   date or hours and minutes, then a Timezone must be specified or
        #   assumed. The default is always GMT. So creation operations which
        #   don't pass any Timezone assume the date, hours and minutes are GMT.
        #   The TimeLibrary does not use the default TimeZone operation in Java,
        #   the selection of the appropriate Timezone is left to the application.
        gmt_10_hour = TimePoint.at(2004, 3, 5, 10, 10, 0, 0, zone=self.gmt)
        default_10_hour = TimePoint.at_GMT(2004, 3, 5, 10, 10, 0, 0)
        pt_2_hour = TimePoint.at(2004, 3, 5, 2, 10, 0, 0, zone=self.pt)
        assert_that(default_10_hour, equal_to(gmt_10_hour))
        assert_that(pt_2_hour, equal_to(gmt_10_hour))

        gmt_6_hour = TimePoint.at(2004, 3, 5, 6, 0, 0, 0, self.gmt)
        ct_0_hour = TimePoint.at(2004, 3, 5, 0, 0, 0, 0, self.ct)
        ct_midnight = TimePoint.at_midnight(2004, 3, 5, self.ct)
        assert_that(gmt_6_hour, equal_to(ct_0_hour))
        assert_that(gmt_6_hour, equal_to(ct_midnight))

    def testStringFormat(self):
        point = TimePoint.at(2004, 3, 12, 5, 3, 14, 0, self.pt)
        # Try stupid date/time format, so that it couldn't work by accident.
        assert_that(point.to_string("%-m-%y-%d %-M:%-H:%-S", self.pt), equal_to("3-04-12 3:5:14"))
        assert_that(point.to_string("%-m-%y-%d", self.pt), equal_to("3-04-12"))

