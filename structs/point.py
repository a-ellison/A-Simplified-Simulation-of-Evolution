import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, n):
        return Point(self.x + n, self.y + n)

    def move_to(self, distance, angle):
        new_x = self.x + math.cos(angle) * distance
        new_y = self.y + math.sin(angle) * distance
        return Point(new_x, new_y)

    def restrict_to(self, min_coordinate, max_coordinate):
        x = max(min_coordinate.x, min(self.x, max_coordinate.x))
        y = max(min_coordinate.y, min(self.y, max_coordinate.y))
        return Point(x, y)

    def distance_to(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to(self, target):
        dx = target.x - self.x
        if dx == 0:
            return 0
        dy = target.y - self.y
        return math.atan2(dy, dx)

    def find_closest(self, objects, get_position=lambda obj: obj):
        min_distance = float('inf')
        closest = None
        for obj in objects:
            distance = self.distance_to(get_position(obj))
            if distance < min_distance:
                min_distance = distance
                closest = obj
        return closest

    @classmethod
    def random(cls, min_coordinate, max_coordinate, side=None):
        if side == 'top':
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = min_coordinate.y
        elif side == 'right':
            x = max_coordinate.x
            y = random.randint(min_coordinate.y, max_coordinate.y)
        elif side == 'bottom':
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = max_coordinate.y
        elif side == 'left':
            x = min_coordinate.x
            y = random.randint(min_coordinate.y, max_coordinate.y)
        else:
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = random.randint(min_coordinate.y, max_coordinate.y)
        return Point(x, y)
