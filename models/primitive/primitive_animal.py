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


class PrimitiveAnimal(drawable.Drawable):
    def __init__(self, x, y, size, color, speed, direction, max_energy, sight_range):
        super().__init__(x, y, size, color)
        self.speed = speed
        self.direction = direction
        self.max_energy = max_energy
        self.sight_range = sight_range
        self.objective = None

    def move(self, max_x, max_y):
        self.last_x = self.x
        self.last_y = self.y
        target_x = self.objective.x
        target_y = self.objective.y
        distance_to_target = helper_functions.distance_to(self.x, self.y, target_x, target_y)
        distance = min(self.speed, distance_to_target)
        angle = helper_functions.angle_to(self.x, self.y, target_x, target_y)
        dx = cos(angle) * distance
        logging.info(f'x changed from {self.x} to {self.x + dx}')
        self.x += dx
        dy = sin(angle) * distance
        logging.info(f'y changed from {self.y} to {self.y + dy}')
        self.y += dy
        self.x, self.y = helper_functions.restrict_position(self.x, self.y, max_x, max_y)

    def add_objective(self, new_objective):
        if self.objective is None:
            self.objective = new_objective
        elif new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    @classmethod
    def random(cls, max_x, max_y, color=Color.random()):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        speed = helper_functions.random_decimal(MIN_SPEED, MAX_SPEED, DECIMAL_PLACES)
        size = helper_functions.random_decimal(MIN_SIZE, MAX_SIZE, DECIMAL_PLACES)
        direction = random.randint(0, 360)
        max_energy = 99
        sight_range = 99
        return PrimitiveAnimal(x, y, size, color, speed, direction, max_energy, sight_range)
