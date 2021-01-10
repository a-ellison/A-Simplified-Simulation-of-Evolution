import math
import random


class Point:
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_by(self, n1, n2=None):
        if n2 is not None:
            return Point(self.x + n1, self.y + n2)
        return Point(self.x + n1, self.y + n1)

    def translate(self, n1, n2=None):
        if n2 is not None:
            return Point(self.x * n1, self.y * n2)
        return Point(self.x * n1, self.y * n1)

    def move_to(self, distance, angle):
        new_x = self.x + math.cos(angle) * distance
        new_y = self.y + math.sin(angle) * distance
        return Point(new_x, new_y)

    def restrict_to(self, min_coordinate, max_coordinate, side_switch=False):
        if side_switch:
            if self.x < min_coordinate.x:
                x = max_coordinate.x
            elif self.x > max_coordinate.x:
                x = min_coordinate.x
            else:
                x = self.x
            if self.y < min_coordinate.y:
                y = max_coordinate.y
            elif self.y > max_coordinate.y:
                y = min_coordinate.y
            else:
                y = self.y
        else:
            x = max(min_coordinate.x, min(self.x, max_coordinate.x))
            y = max(min_coordinate.y, min(self.y, max_coordinate.y))
        return Point(x, y)

    def distance_to(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def angle_to(self, target):
        dx = target.x - self.x
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
        min_coordinate = min_coordinate.to_int()
        max_coordinate = max_coordinate.to_int()
        if side == Point.TOP:
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = min_coordinate.y
        elif side == Point.RIGHT:
            x = max_coordinate.x
            y = random.randint(min_coordinate.y, max_coordinate.y)
        elif side == Point.BOTTOM:
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = max_coordinate.y
        elif side == Point.LEFT:
            x = min_coordinate.x
            y = random.randint(min_coordinate.y, max_coordinate.y)
        else:
            x = random.randint(min_coordinate.x, max_coordinate.x)
            y = random.randint(min_coordinate.y, max_coordinate.y)
        return Point(x, y)

    def to_int(self):
        return Point(int(self.x), int(self.y))

    def copy(self):
        return Point(self.x, self.y)

    def __str__(self):
        return f'Point({self.x}, {self.y})'
