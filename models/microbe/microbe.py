import logging
import random
from enum import Enum

from models.drawable import Drawable
from structs.color import Color
from structs.point import Point


class Direction(Enum):
    NW = 0
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7

    def next_position(self, position):
        if self.name == 'NW':
            return position.move_by(-1, 1)
        elif self.name == 'N':
            return position.move_by(0, 1)
        elif self.name == 'NE':
            return position.move_by(1, 1)
        elif self.name == 'W':
            return position.move_by(-1, 0)
        elif self.name == 'E':
            return position.move_by(1, 0)
        elif self.name == 'SW':
            return position.move_by(-1, -1)
        elif self.name == 'S':
            return position.move_by(0, -1)
        elif self.name == 'SE':
            return position.move_by(1, -1)

    @classmethod
    def steering_cost(cls, old, new):
        diff = abs(old.value - new.value)
        if diff == 0:
            return 0
        if diff <= 4:
            x = diff
        elif diff > 4:
            x = 8 - diff
        return - 2 ** (x - 1)

    def steer(self, new):
        return Direction((self.value + new.value) % 8)


class Microbe(Drawable):
    FOOD_ENERGY = 40
    MAX_ENERGY = 1500
    REPRODUCTION_ENERGY = 1000
    STEP_COST = 1
    CELL_SIZE = 5

    def __init__(self, cell_position, probabilities, color=Color(0, 0, 255)):
        self.cell_position = cell_position
        super().__init__(Microbe.to_actual_position(self.cell_position), Microbe.CELL_SIZE / 2, color)
        self.probabilities = probabilities
        self.direction = Direction(self.probabilities.index(max(self.probabilities)))
        self.energy = 100
        self.age = 0

    def move(self, min_cell, max_cell):
        self.cell_position = self.direction.next_position(self.cell_position).restrict_to(min_cell, max_cell, True)
        self.update_position()
        self.energy -= Microbe.STEP_COST
        self.age += 1

    @classmethod
    def to_actual_position(cls, cell_position):
        x = cell_position.x * Microbe.CELL_SIZE + Microbe.CELL_SIZE / 2
        y = cell_position.y * Microbe.CELL_SIZE + Microbe.CELL_SIZE / 2
        return Point(x, y)

    def update_position(self):
        self.position = Microbe.to_actual_position(self.cell_position)

    def change_direction(self):
        r = random.random()
        old_direction = self.direction
        self.direction = self.get_new_direction(r)
        self.energy += Direction.steering_cost(old_direction, self.direction)

    def get_new_direction(self, r):
        i = None
        for k in range(len(self.probabilities)):
            p = self.probabilities[k]
            if i is None or r >= p > self.probabilities[i]:
                i = k
        return self.direction.steer(Direction(i))

    @property
    def is_alive(self):
        return self.energy > 0

    @property
    def can_reproduce(self):
        return self.energy >= Microbe.REPRODUCTION_ENERGY

    @property
    def is_hungry(self):
        return self.energy < Microbe.MAX_ENERGY

    @classmethod
    def _random_probabilities(cls):
        probabilities = []
        for i in range(8):
            r = random.random()
            probabilities.append(r)
        return _normalize_probabilities(probabilities)

    def eat(self, food):
        self.energy += food.energy

    @classmethod
    def random(cls, min_cell, max_cell, **kwargs):
        cell_position = kwargs.get('cell_position')
        if cell_position is None:
            cell_position = Point.random(min_cell, max_cell)
        probabilities = kwargs.get('probabilities')
        if probabilities is None:
            probabilities = Microbe._random_probabilities()
        return Microbe(cell_position.to_int(), probabilities)

    def mutate(self):
        self.energy /= 2
        index = random.randint(0, 7)
        r = random.random() - 0.5
        new_probabilities = self.probabilities.copy()
        new_probabilities[index] = max(0, new_probabilities[index] + r)
        new_probabilities = _normalize_probabilities(new_probabilities)
        return Microbe(self.cell_position.copy(), new_probabilities)


def _normalize_probabilities(probabilities):
    s = sum(probabilities)
    return [p / s for p in probabilities]

