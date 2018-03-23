class Ratio:
    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator

    @staticmethod
    def of(numerator, denominator):
        #porting from Java, enforcing float type
        return Ratio(numerator+0.0, denominator+0.0)

    