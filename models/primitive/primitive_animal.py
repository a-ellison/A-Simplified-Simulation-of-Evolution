import logging
import random
from math import cos
from math import sin

from models import drawable
from structs.color import Color

import helper_functions


DECIMAL_PLACES = 2
MIN_SIZE = 500 / 10 ** DECIMAL_PLACES
MAX_SIZE = 600 / 10 ** DECIMAL_PLACES
MIN_SPEED = 150 / 10 ** DECIMAL_PLACES
MAX_SPEED = 240 / 10 ** DECIMAL_PLACES
MIN_SIGHT_RANGE = 1
MAX_SIGHT_RANGE = 3


class PrimitiveAnimal(drawable.Drawable):
    def __init__(self, x, y, size, color, speed, direction, max_energy, sight_range):
        super().__init__(x, y, size, color)
        self.age = 0
        self.speed = speed
        self.max_energy = max_energy
        self.energy = max_energy
        self.sight_range = sight_range
        self.objective = None
        self.last_objective = None

    def move(self, max_x, max_y):
        self.last_x = self.x
        self.last_y = self.y
        self.last_objective = self.objective
        distance_to_target = helper_functions.distance_to(self.x, self.y, self.objective.x, self.objective.y)
        distance = min(self.speed, distance_to_target)
        angle = self.angle_to_objective()
        dx = cos(angle) * distance
        self.x += dx
        dy = sin(angle) * distance
        self.y += dy
        self.x, self.y = helper_functions.restrict_position(self.x, self.y, max_x, max_y, radius=self.size)
        self.last_objective = self.objective
        self.objective = None
        # logging.info(f'energy cost: {helper_functions.distance_to(self.last_x, self.last_y, self.x, self.y) * self.size}')

    def angle_to_objective(self):
        return helper_functions.angle_to(self.x, self.y, self.objective.x, self.objective.y)

    @property
    def has_moved(self):
        return self.last_objective is not None

    def can_see(self, drawable: drawable.Drawable):
        return helper_functions.distance_to(self.x, self.y, drawable.x, drawable.y) <= self.sight_range

    def can_reach(self, drawable: drawable.Drawable):
        return helper_functions.distance_to(self.x, self.y, drawable.x, drawable.y) - self.size / 2 < self.size

    def add_objective(self, new_objective):
        if self.objective is None or new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    def consume(self, edible):
        self.energy = min(self.max_energy, self.energy + edible.size)

    @classmethod
    def random(cls, max_x, max_y, side=None, color=Color.random()):
        if side == 'top':
            x = random.randint(0, max_x)
            y = 0
        elif side == 'right':
            x = max_x
            y = random.randint(0, max_y)
        elif side == 'bottom':
            x = random.randint(0, max_x)
            y = max_y
        elif side == 'left':
            x = 0
            y = random.randint(0, max_y)
        else:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
        speed = helper_functions.random_decimal(MIN_SPEED, MAX_SPEED, DECIMAL_PLACES)
        size = helper_functions.random_decimal(MIN_SIZE, MAX_SIZE, DECIMAL_PLACES)
        direction = random.randint(0, 360)
        max_energy = 99
        sight_range = helper_functions.random_decimal(MIN_SIGHT_RANGE, MAX_SIGHT_RANGE, DECIMAL_PLACES) * size
        return PrimitiveAnimal(x, y, size, color, speed, direction, max_energy, sight_range)
