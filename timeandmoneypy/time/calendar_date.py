class CalendarDate(object):

    @staticmethod
    def _from(year, month, day):
        return CalendarDate(year, month, day)

    @staticmethod
    def from_string(date_string, pattern):
        pass

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def is_before(self, other):
        if other is None:
            return False
        if self.year < other.year: return True
        if self.year > other.year: return False
        if self.month < other.month: return True
        if self.month > other.month: return False
        return self.day < other.day

    def is_after(self, other):
        return other is not None and \
               not self.is_before(other) and \
               not self == other

    def __eq__(self, other):
        return other is not None and \
               self.year == other.year and \
               self.month == other.month and \
               self.day == other.day

    def start_as_time_point(self, zone):
        from timeandmoneypy.time import TimePoint
        return TimePoint.at_midnight(self.year, self.month, self.day, zone=zone)

    # def as_time_interval(self, zone):
    #     return TimeInterval.starting_from(self.start_as_time_point(zone), True, )