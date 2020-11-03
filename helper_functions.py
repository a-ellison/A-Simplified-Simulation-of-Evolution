import random
import math


def random_decimal(start, stop, decimal_places=2):
    factor = 10 ** decimal_places
    start = int(start * factor)
    stop = int(stop * factor)
    n = random.randint(start, stop)
    return n / factor


def mutate_value(min_value, max_value, current_value, mutation):
    min_mutation = max(min_value, current_value - mutation)
    max_mutation = min(max_value, current_value + mutation)
    return random_decimal(min_mutation, max_mutation)
