class IntervalMap():

    def put(self, key_interval, value):
        raise NotImplementedError('put interface not implemented on IntervalMap')

    def get(self, key):
        raise NotImplementedError('get interface not implemented on IntervalMap')

    def remove(self, keyInterval):
        raise NotImplementedError('remove interface not implemented on IntervalMap')

    def contains_key(self, key):
        raise NotImplementedError('contains_key interface not implemented on IntervalMap')

    def contains_intersecting_key(self, interval):
        raise NotImplementedError('contains_intersecting_key interface not implemented on IntervalMap')\
