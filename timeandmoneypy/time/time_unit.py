from timeandmoneypy.time.time_unit_conversion_factors import TimeUnitConversionFactors


class Type(object):
    millisecond = None
    second = None
    minute = None
    hour = None
    day = None
    week = None
    month = None
    quarter = None
    year = None

    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        return isinstance(other, Type) and other is not None and self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return self._name

Type.millisecond = Type("millisecond")
Type.second = Type("second")
Type.minute = Type("minute")
Type.hour = Type("hour")
Type.day = Type("day")
Type.week = Type("week")
Type.month = Type("month")
Type.quarter = Type("quarter")
Type.year = Type("year")


class TimeUnit(TimeUnitConversionFactors):

    def __init__(self, type, base_type, factor):
        self._type = type
        self._base_type = base_type
        self._factor = factor

    millisecond = None
    second = None
    minute = None
    hour = None
    day = None
    week = None
    descending_millisecond_based = []
    descending_millisecond_based_for_display = []
    month = None
    quarter = None
    year = None
    descending_month_based = []
    descending_month_based_for_display = []

    def __str__(self):
        return str(self._type)

    def is_convertible_to_milliseconds(self):
        return self.is_convertible_to(self.millisecond);

    def is_convertible_to(self, other):
        return self._base_type == other._base_type

    def compare_to(self, other):
        assert(isinstance(other, TimeUnit))
        if other._base_type == self._base_type:
            return self._factor - other._factor
        if self._base_type == Type.month:
            return 1
        else:
            return -1

    def __eq__(self, other):
        return self.compare_to(other) == 0

    def __cmp__(self, other):
        return self.compare_to(other)

    def descending_units(self):
        return self.descending_millisecond_based if self.is_convertible_to_milliseconds() else self.descending_month_based

    def descending_units_for_display(self):
        return self.descending_millisecond_based_for_display if self.is_convertible_to_milliseconds() else self.descending_month_based_for_display

    def next_finer_unit(self):
        descending = self.descending_units()
        index = -1
        for i in range(0, len(descending)):
            if descending[i] == self:
                index = i
        if index == len(descending)-1:
            return None
        return descending[index + 1]

TimeUnit.millisecond = TimeUnit(Type.millisecond, Type.millisecond, 1)
TimeUnit.second = TimeUnit(Type.second, Type.millisecond, TimeUnitConversionFactors.milliseconds_per_second)
TimeUnit.minute = TimeUnit(Type.minute, Type.millisecond, TimeUnitConversionFactors.milliseconds_per_minute)
TimeUnit.hour = TimeUnit(Type.hour, Type.millisecond, TimeUnitConversionFactors.milliseconds_per_hour)
TimeUnit.day = TimeUnit(Type.day, Type.millisecond, TimeUnitConversionFactors.milliseconds_per_day)
TimeUnit.week = TimeUnit(Type.week, Type.millisecond, TimeUnitConversionFactors.milliseconds_per_week)
TimeUnit.descending_millisecond_based = [TimeUnit.week,
                                         TimeUnit.day,
                                         TimeUnit.hour,
                                         TimeUnit.minute,
                                         TimeUnit.second,
                                         TimeUnit.millisecond]
TimeUnit.descending_millisecond_based_for_display = [TimeUnit.day,
                                                     TimeUnit.hour,
                                                     TimeUnit.minute,
                                                     TimeUnit.second,
                                                     TimeUnit.millisecond]
TimeUnit.month = TimeUnit(Type.month, Type.month, 1)
TimeUnit.quarter = TimeUnit(Type.quarter, Type.month, TimeUnitConversionFactors.months_per_quarter)
TimeUnit.year = TimeUnit(Type.year, Type.month, TimeUnitConversionFactors.months_per_year)
TimeUnit.descending_month_based = [TimeUnit.year, TimeUnit.quarter, TimeUnit.month]
TimeUnit.descending_month_based_for_display = [TimeUnit.quarter, TimeUnit.month]