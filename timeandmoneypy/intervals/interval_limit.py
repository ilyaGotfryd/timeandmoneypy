class IntervalLimit():
    def __init__(self, closed, lower, value):
        self._closed = closed
        self._lower = lower
        self._value = value

    @staticmethod
    def upper(closed, value):
        return IntervalLimit(closed, False, value)

    @staticmethod
    def lower(closed, value):
        return IntervalLimit(closed, True, value)

    def is_lower(self):
        return self._lower

    def is_upper(self):
        return not self._lower

    def is_closed(self):
        return self._closed

    def is_opened(self):
        return not self._closed

    def get_value(self):
        return self._value

    def compare_to(self, other):
        if other is not None and isinstance(other, IntervalLimit):
            if other.get_value() == self._value:
                return 0
            if self._value is None:
                return -1 if self._lower else 1
            if other.get_value() is None:
                return 1 if other.is_lower() else -1
            return -1 if self._value < other.get_value() else \
                    1 if self._value > other.get_value() else 0
        raise TypeError('Expected IntervalLimit but was of type {}'.format(other.__class__.__name__) )

    def __cmp__(self, other):
        return self.compare_to(other)

    def __eq__(self, other):
        return self.compare_to(other) == 0

    def __ne__(self, other):
        return self.compare_to(other) != 0

    def __lt__(self, other):
        return self.compare_to(other) == -1

    def __gt__(self, other):
        return self.compare_to(other) == 1

    def __ge__(self, other):
        return self.compare_to(other) in [1,0]

    def __le__(self, other):
        return self.compare_to(other) in [-1,0]

    def __hash__(self):
        return hash((self._closed, self._lower, hash(str(self._value))))
