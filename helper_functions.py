import random
import math


def random_decimal(start, stop, decimal_places):
    factor = 10 ** decimal_places
    start = int(start * factor)
    stop = int(stop * factor)
    n = random.randint(start, stop)
    return n / factor


def get_new_position(old_x, old_y, direction, distance):
    radians = to_radians(direction)
    new_x = old_x + math.cos(radians) * distance
    new_y = old_y + math.sin(radians) * distance
    return new_x, new_y


def to_radians(degrees):
    return degrees * math.pi / 180


def restrict_position(x, y, max_x, max_y, radius=0):
    x = min(x + radius, max_x)
    x = max(0, x - radius)
    y = min(y + radius, max_y)
    y = max(0, y - radius)
    return x, y


def distance_to(x, y, target_x, target_y):
    dx = target_x - x
    dy = target_y - y
    return math.sqrt(dx**2 + dy**2)


def angle_to(x, y, target_x, target_y):
    dx = target_x - x
    if dx == 0:
        return 0
    dy = target_y - y
    return math.atan(dy / dx)

