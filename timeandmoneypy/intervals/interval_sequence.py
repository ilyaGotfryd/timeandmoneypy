class IntervalSequence():

    def __init__(self):
        self._intervals = []

    def __iter__(self):
        return iter(self._intervals)

    def add(self, interval):
        self._intervals.append(interval)
        self._intervals.sort(lambda a, b: a.compare_to(b))

    def is_empty(self):
        return len(self._intervals) == 0

    def gaps(self):
        gaps = IntervalSequence()
        if len(self._intervals) < 2:
            return IntervalSequence()
        for i in range(1, len(self._intervals)):
            left = self._intervals[i - 1]
            right = self._intervals[i]
            gap = left.gap(right)
            if not gap.is_empty():
                gaps.add(gap)
        return gaps

    def extent(self):
        if self.is_empty():
            return None
        ## TODO: Add a creation method to Interval for empty(), if it can be
        ## polymorphic.
        if len(self._intervals) == 1:
            return self._intervals[0]
        left = self._intervals[0]
        right = self._intervals[-1]
        return left.new_of_same_type(left.lower_limit(), left.includes_lower_limit(), right.upper_limit(), right.includes_upper_limit())