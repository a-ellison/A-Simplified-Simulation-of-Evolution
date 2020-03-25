import random


class Functions(object):
    @classmethod
    def uniform(cls, low, high, factor):
        low = int(low * factor)
        high = int(high * factor)
        n = random.randint(low, high)
        return n / factor
