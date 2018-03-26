from interval_limit import IntervalLimit

def local_compare_to(a, b):
    return -1 if a < b else 1 if a > b else 0

class Interval:

    @staticmethod
    def closed(lower, upper):
        return Interval(lower, True, upper, True)

    @staticmethod
    def open(lower, upper):
        return Interval(lower, False, upper, False)

    @staticmethod
    def over(lower, lower_included, upper, upper_included):
        return Interval(lower, lower_included, upper, upper_included)

    def __init__(self, *args):
        assert len(args) == 2 or len(args) == 4
        if len(args) == 2:
            self._create_with_intervals(*args)
        elif len(args) == 4:
            self._create_with_boundaries(*args)

    def _create_with_intervals(self, lower, upper):
        assert isinstance(lower, IntervalLimit)
        assert isinstance(upper, IntervalLimit)
        assert lower.is_lower()
        assert upper.is_upper()
        assert lower.compare_to(upper) <= 0
        self._lower_limit_object = lower
        self._upper_limit_object = upper

    def _create_with_boundaries(self, lower, is_lower_closed, upper, is_upper_closed):
        self._create_with_intervals(IntervalLimit.lower(is_lower_closed, lower),
                                    IntervalLimit.upper(is_upper_closed, upper))

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other):
        if other is None:
            return False
        this_empty = self.is_empty()
        other_empty = other.is_empty()
        if this_empty and other_empty:
            return True
        if this_empty != other_empty:
            return False
        this_single = self.is_single_element()
        other_single = other.is_single_element()
        if this_single and other_single:
            return self.lower_limit().equals(other.lower_limit())
        if this_single != other_single:
            return False
        return self.compare_to(other) == 0

    def new_of_same_type(self, lower,  is_lower_closed, upper, is_upper_closed):
        return Interval(lower, is_lower_closed, upper, is_upper_closed)

    def compare_to(self, other):
        if not self.upper_limit() == other.upper_limit():
            return local_compare_to(self.upper_limit(), other.upper_limit())
        if self.includes_lower_limit() and not other.includes_lower_limit():
            return -1
        if not self.includes_lower_limit() and other.includes_lower_limit():
            return 1
        return local_compare_to(self.lower_limit(), other.lower_limit())

    def is_open(self):
        return not self.includes_lower_limit() and not self.includes_upper_limit()

    def is_closed(self):
        return self.includes_lower_limit() and self.includes_upper_limit()

    def is_empty(self):
        return self.is_open() and self.upper_limit() == self.lower_limit()

    def upper_limit(self):
        return self._upper_limit_object.get_value()

    def includes_upper_limit(self):
        return self._upper_limit_object.is_closed()

    def has_upper_limit(self):
        return self._upper_limit_object is not None

    def lower_limit(self):
        return self._lower_limit_object.get_value()

    def includes_lower_limit(self):
        return self._lower_limit_object.is_closed()

    def has_lower_limit(self):
        return self._lower_limit_object is not None

    def is_single_element(self):
        return self.upper_limit() == self.lower_limit() and not self.is_empty()

    def is_below(self, value):
        if not self.has_upper_limit():
            return False
        comparison = local_compare_to(self.upper_limit(), value)
        return comparison < 0 or (comparison == 0 and not self.includes_upper_limit())

    def is_above(self, value):
        if not self.has_lower_limit():
            return False
        comparison = local_compare_to(self.lower_limit(), value)
        return comparison > 0 or (comparison == 0 and not self.includes_lower_limit())

    def includes(self, value):
        return not self.is_below(value) and not self.is_above(value)
