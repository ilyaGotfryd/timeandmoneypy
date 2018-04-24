from timeandmoneypy.intervals.interval_map import IntervalMap

class LinearIntervalMap(IntervalMap):

    def __init__(self):
        self._key_values = {}

    def put(self, key_interval, value):
        self.remove(key_interval)
        self._key_values[key_interval] = value

    def remove(self, key_interval):
        interval_sequence = self.intersecting_keys(key_interval)
        for interval in interval_sequence:
            old_value = self._key_values.get(interval)
            del self._key_values[interval]
            complement_interval_sequence = key_interval.complement_relative_to(interval)
            self._direct_put(complement_interval_sequence, old_value)

    def _direct_put(self, interval_sequence, value):
        for interval in interval_sequence:
            self._key_values[interval] = value

    def get(self, key):
        key_interval = self.find_key_interval_containing(key)
        return self._key_values.get(key_interval)

    def contains_key(self, key):
        return self.find_key_interval_containing(key) is not None

    def find_key_interval_containing(self, key):
        if key is None:
            return None
        for interval in self._key_values.keys():
            if interval.includes(key):
                return interval
        return None

    def intersecting_keys(self, other_interval):
        interval_sequence = []
        for key_interval in self._key_values.keys():
            if key_interval.intersects(other_interval):
                interval_sequence.append(key_interval)
        return interval_sequence

    def contains_intersecting_key(self, other_interval):
        return not len(self.intersecting_keys(other_interval)) == 0
