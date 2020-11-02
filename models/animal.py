import logging
import random
import math

from models.drawable import Drawable
from structs.color import Color

import helper_functions
from structs.point import Point

MIN_SIZE = 300 / 10 ** 2
MAX_SIZE = 500 / 10 ** 2
MIN_SPEED = 150 / 10 ** 2
MAX_SPEED = 240 / 10 ** 2
MIN_SIGHT_RANGE = 10
MAX_SIGHT_RANGE = 30


class Animal(Drawable):
    def __init__(self, position: Point, radius, color: Color, speed, max_energy, sight_range):
        super().__init__(position, radius, color)
        self.age = 0
        self.speed = speed
        self.max_energy = max_energy
        self.energy = max_energy
        self.sight_range = sight_range
        self.objective = None
        self.last_objective = None
        self.foods_eaten = 0

    def move(self, min_coordinate, max_coordinate):
        self.last_position = self.position
        self.last_objective = self.objective
        distance_to_target = self.position.distance_to(self.objective.position)
        distance = min(self.speed, distance_to_target)
        angle = self.position.angle_to(self.objective.position)
        min_coordinate = min_coordinate.move_by(self.radius)
        max_coordinate = max_coordinate.move_by(-self.radius)
        self.position = self.position.move_to(distance, angle).restrict_to(min_coordinate, max_coordinate)
        self.last_objective = self.objective
        self.objective = None

    @property
    def mass(self):
        return self.radius ** 3

    @property
    def step_cost(self):
        distance_moved = self.position.distance_to(self.last_position)
        movement_cost = 0.5 * self.mass * (distance_moved ** 2)
        return movement_cost + self.sight_range

    def apply_step_cost(self):
        self.energy -= self.step_cost

    @property
    def has_moved(self):
        return self.last_objective is not None

    @property
    def is_alive(self):
        return self.energy > 0

    def can_see(self, position: Point):
        return self.position.distance_to(position) <= self.sight_range

    def can_reach(self, position: Point):
        return self.position.distance_to(position) - self.radius < self.radius * 2

    def add_objective(self, new_objective):
        if self.objective is None or new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    def eat(self, edible):
        self.foods_eaten += 1
        self.energy = min(self.max_energy, self.energy + edible.radius)

    @classmethod
    def random(cls, min_coordinate, max_coordinate, side=None, color=Color.random()):
        radius = helper_functions.random_decimal(MIN_SIZE, MAX_SIZE)
        min_x = math.ceil(min_coordinate.x + radius)
        min_y = math.ceil(min_coordinate.y + radius)
        max_x = math.ceil(max_coordinate.x - radius)
        max_y = math.ceil(max_coordinate.y - radius)
        if side == 'top':
            x = random.randint(min_x, max_x)
            y = min_y
        elif side == 'right':
            x = max_x
            y = random.randint(min_y, max_y)
        elif side == 'bottom':
            x = random.randint(min_x, max_x)
            y = max_y
        elif side == 'left':
            x = min_x
            y = random.randint(min_y, max_y)
        else:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
        speed = helper_functions.random_decimal(MIN_SPEED, MAX_SPEED)
        max_energy = 99
        sight_range = helper_functions.random_decimal(MIN_SIGHT_RANGE, MAX_SIGHT_RANGE)
        return Animal(Point(x, y), radius, color, speed, max_energy, sight_range)
