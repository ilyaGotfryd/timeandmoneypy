import pytz
from datetime import datetime, tzinfo, timedelta



class TimePoint(object):
    _GMT = pytz.timezone('GMT')
    _epoch = _GMT.localize(datetime.utcfromtimestamp(0))

    @classmethod
    def at_midnight_GMT(cls, year, month, date):
        return cls.at_midnight(year, month, date, cls._GMT)

    @classmethod
    def at_midnight(cls, year, month, date, zone):
        return cls.at(year, month, date, 0, 0, 0, 0, zone)

    @classmethod
    def at_GMT(cls, year, month, date, hour, minute, second=0, millisecond=0):
        return cls.at(year, month, date, hour, minute, second, millisecond, cls._GMT)

    @classmethod
    def at_12_hr(cls, year, month, date, hour, am_pm, minute, second, millisecond, zone):
        return cls.at(year, month, date, cls.converted_to_24_hour(hour, am_pm), minute, second, millisecond, zone)

    @classmethod
    def converted_to_24_hour(cls, hour, am_pm):
        translated_am_pm = 0 if "AM".lower() == am_pm.lower() else 12
        translated_am_pm -= 12 if hour == 12 else 0
        return hour + translated_am_pm

    @classmethod
    def at(cls, year, month, date, hour, minute, second=0, millisecond=0, zone=None):
        zone = cls._GMT if zone is None else zone
        assert(isinstance(zone, tzinfo))
        return cls._from(zone.localize(datetime(year=year, month=month, day=date, hour=hour, minute=minute,
                        second=second, microsecond=millisecond)))

    @classmethod
    def parse_GMT_from( cls, date_string, pattern):
        return cls.parse_from(date_string, pattern, cls._GMT)

    @classmethod
    def parse_from(cls, date_string, pattern, zone):
        assert(isinstance(date_string, str) and isinstance(pattern, str) and isinstance(zone, tzinfo))
        unaware = datetime.strptime(date_string, pattern)
        return cls._from(unaware.replace(tzinfo=zone))

    @classmethod
    def _from(cls, value):
        if isinstance(value, datetime):
            timestamp = (value - cls._epoch).total_seconds() * 1000.0
            return TimePoint(timestamp)
        elif isinstance(value, int):
            return TimePoint(value)

    def to_string(self, format_string=None, zone=None):
        if format_string is None:
            str(self.as_datetime())
        if zone is None:
            return self.as_datetime().strftime(format_string)
        return zone.normalize(self.as_datetime()).strftime(format_string)

    def as_datetime(self):
        return self._epoch + timedelta(milliseconds=self._milliseconds_from_epoch)

    def back_to_midnight(self, zone):
        raise NotImplemented("TimePoint.back_to_midnight(zone) is not implemented.")

    def __init__(self, milliseconds):
        self._milliseconds_from_epoch = milliseconds

    def __eq__(self, other):
        return isinstance(other, TimePoint) and \
               other._milliseconds_from_epoch == self._milliseconds_from_epoch

    def __hash__(self):
        return int(self._milliseconds_from_epoch)

