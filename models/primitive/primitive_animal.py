import random
from math import cos
from math import sin

from structs.color import Color

import helper_functions


DECIMAL_PLACES = 2
MIN_SIZE = 150 / 10 ** DECIMAL_PLACES
MAX_SIZE = 240 / 10 ** DECIMAL_PLACES
MIN_SPEED = 150 / 10 ** DECIMAL_PLACES
MAX_SPEED = 240 / 10 ** DECIMAL_PLACES


class PrimitiveAnimal(object):
    def __init__(self, x, y, speed: int, color, size: int, direction: int, max_energy: int, sight_range: int):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.size = size
        self.direction = direction
        self.max_energy = max_energy
        self.sight_range = sight_range
        self.objective = None

    def move(self):
        distance = self.speed
        angle = self.direction
        dx = cos(angle) * distance
        self.x += dx
        dy = sin(angle) * distance
        self.y += dy

    def add_objective(self, new_objective):
        if self.objective is None:
            self.objective = new_objective
        elif new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    @classmethod
    def random(cls, max_x, max_y):
        x = random.randint(max_x)
        y = random.randint(max_y)
        speed = helper_functions.random_decimal(MIN_SPEED, MAX_SPEED, DECIMAL_PLACES)
        color = Color.random()
        size = helper_functions.random_decimal(MIN_SIZE, MAX_SIZE, DECIMAL_PLACES)
        direction = random.randint(0, 360)
        max_energy = 99
        sight_range = 99
        return PrimitiveAnimal(x, y, speed, color, size, sight_range, direction, max_energy)
