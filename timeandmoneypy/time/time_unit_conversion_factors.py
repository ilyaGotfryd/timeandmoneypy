

class TimeUnitConversionFactors:
    milliseconds_per_second = 1000
    milliseconds_per_minute = 60 * milliseconds_per_second
    milliseconds_per_hour = 60 * milliseconds_per_minute
    milliseconds_per_day = 24 * milliseconds_per_hour
    milliseconds_per_week = 7 * milliseconds_per_day
    months_per_quarter = 3
    months_per_year = 12

    def __init__(self):
        pass
