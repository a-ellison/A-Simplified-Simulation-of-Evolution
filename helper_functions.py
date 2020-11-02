import random
import math


def random_decimal(start, stop, decimal_places=2):
    factor = 10 ** decimal_places
    start = int(start * factor)
    stop = int(stop * factor)
    n = random.randint(start, stop)
    return n / factor

