import random
from enum import Enum


class Direction(Enum):
    NW = 0
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7

    @classmethod
    def random(cls):
        return Direction(random.randint(0, 7))

    def steer(self, value):
        direction = self.value + value % 8
        return Direction(direction)

    def move(self, start):
        if self.name == 'NW':
            return start.move_by(-1, 1)
        elif self.name == 'N':
            return start.move_by(0, 1)
        elif self.name == 'NE':
            return start.move_by(1, 1)
        elif self.name == 'W':
            return start.move_by(-1, 0)
        elif self.name == 'E':
            return start.move_by(1, 0)
        elif self.name == 'SW':
            return start.move_by(-1, -1)
        elif self.name == 'S':
            return start.move_by(0, -1)
        elif self.name == 'SE':
            return start.move_by(1, -1)
