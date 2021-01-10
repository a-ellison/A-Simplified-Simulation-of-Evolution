import logging
import math
import random
import time
from enum import Enum

from helpers import Speed
from models.behavior_base import BehaviorBase
from models.drawable import Drawable
from models.microbe.data import MicrobeData
from models.microbe.microbe import Microbe
from structs.color import Color
from structs.point import Point

START_MICROBE_NUM = 10
START_FOOD_NUM = 100
FOOD_PER_STEP = 2
MICROBES = 'MICROBES'
FOOD = 'FOOD'

FoodPattern = Enum('FoodPattern', 'EVEN SQUARE LINES')


class MicrobeBehavior(BehaviorBase):
    @classmethod
    def initialize(cls, world):
        cls.set_food_matrix(world)
        world[MICROBES] = []
        cls.generate_microbes(world.config['start_population'], world)
        world[FOOD] = []
        cls.generate_food(world.config['start_food'], world)

    @classmethod
    def generate_microbes(cls, n, world):
        for i in range(n):
            m = cls.generate_microbe(world)
            world[MICROBES].append(m)

    @classmethod
    def generate_microbe(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        return Microbe.random(min_cell, max_cell)

    @classmethod
    def to_cell_corners(cls, min_coordinate, max_coordinate):
        return cls.to_cell_position(min_coordinate), cls.to_cell_position(max_coordinate.move_by(-1))

    @classmethod
    def to_cell_position(cls, position):
        return position.translate(1 / Microbe.CELL_SIZE).to_int()

    @classmethod
    def generate_food(cls, n, world):
        pattern = FoodPattern[world.config['food_pattern']]
        if pattern == FoodPattern.EVEN:
            cls.generate_food_even(n, world)
        elif pattern == FoodPattern.SQUARE:
            cls.generate_food_square(n, world)
        elif pattern == FoodPattern.LINES:
            count = math.ceil(n / 10)
            cls.generate_food_even(count, world)
            cls.generate_food_lines(n - count, world)

    @classmethod
    def generate_food_even(cls, n, world):
        for i in range(n):
            min_cell, max_cell = cls.to_cell_corners(*world.corners)
            cell_position = Point.random(min_cell, max_cell)
            cls.add_food(Food(cell_position), world)

    @classmethod
    def add_food(cls, f, world):
        food_matrix = world.store[FOOD]
        world[FOOD].append(f)
        food_matrix[f.cell_position.y][f.cell_position.x].append(f)

    @classmethod
    def generate_food_square(cls, n, world):
        cells_x = int(world.width / Microbe.CELL_SIZE)
        cells_y = int(world.height / Microbe.CELL_SIZE)
        count = math.ceil(n / 8)
        for i in range(count):
            min_cell, max_cell = cls.to_cell_corners(*world.corners)
            r = random.randint(0, 3)
            if r + (i + 1) % 2 == 0:
                continue
            # top
            if r == 0:
                min_cell = min_cell.move_by(cells_x / 8, 0).to_int()
                max_cell = max_cell.move_by(-1 / 8 * cells_x, -7 / 8 * cells_y).to_int()
            # right
            elif r == 1:
                min_cell = min_cell.move_by(7 / 8 * cells_x, 0).to_int()
            # bottom
            elif r == 2:
                min_cell = min_cell.move_by(cells_x / 8, 7 / 8 * cells_y).to_int()
                max_cell = max_cell.move_by(-1 / 8 * cells_x, 0).to_int()
            # left
            else:
                max_cell = Point(min_cell.x + cells_x / 8, max_cell.y).to_int()
            food = Food(Point.random(min_cell, max_cell))
            cls.add_food(food, world)

        center_cell = cls.to_cell_position(world.center)
        square_min_cell = center_cell.move_by(-int(cells_x / 16), -int(cells_y / 16))
        square_max_cell = center_cell.move_by(int(cells_x / 16), int(cells_y / 16))
        for i in range(n - count):
            random_square_cell = Point.random(square_min_cell, square_max_cell)
            cls.add_food(Food(random_square_cell), world)

    @classmethod
    def generate_food_lines(cls, n, world):
        cells_x = int(world.width / Microbe.CELL_SIZE)
        cells_y = int(world.height / Microbe.CELL_SIZE)
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        for i in range(n):
            k = random.randint(1, 5)
            if i % 2 == 0:
                x = cells_x / 6 * k
                y = random.randint(min_cell.y, max_cell.y)
            else:
                x = random.randint(min_cell.x, max_cell.x)
                y = cells_y / 6 * k
            food = Food(Point(x, y).to_int())
            cls.add_food(food, world)

    @classmethod
    def set_food_matrix(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        food_matrix = [[[] for i in range(min_cell.x, max_cell.x + 1)] for k in range(min_cell.y, max_cell.y + 1)]
        world.store[FOOD] = food_matrix

    @classmethod
    def get_config(cls):
        return {
            'start_population': {
                'default': START_MICROBE_NUM,
                'label': 'Start Population:',
            },
            'start_food': {
                'default': START_FOOD_NUM,
                'label': 'Start Food:',
            },
            'food_per_step': {
                'default': FOOD_PER_STEP,
                'label': 'New food per step:',
            },
            'food_pattern': {
                'label': 'Food generation pattern:',
                'type': 'radio',
                'options': [e.name for e in list(FoodPattern)]
            }
        }

    @classmethod
    def get_data_collector(cls, world):
        return MicrobeData(world)

    @classmethod
    def apply(cls, world, speed):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        start = time.perf_counter()
        cls.generate_food(world.config['food_per_step'], world)
        for microbe in world[MICROBES].copy():
            microbe.move(min_cell, max_cell)
            if microbe.is_hungry:
                cls.try_eat(microbe, world)
            microbe.change_direction()
            if microbe.can_reproduce:
                world[MICROBES].append(microbe.mutate())
            elif not microbe.is_alive:
                world[MICROBES].remove(microbe)
                del microbe
        duration = time.perf_counter() - start
        if speed == Speed.SLOW:
            delay = 0.17
        elif speed == Speed.NORMAL:
            delay = 0.017
        elif speed == Speed.FAST:
            delay = 0
        if duration < delay:
            time.sleep(delay - duration)
        return duration

    @classmethod
    def is_dead(cls, world):
        return not len(world[MICROBES])

    @classmethod
    def try_eat(cls, microbe, world):
        if cls.has_food(microbe.cell_position, world):
            microbe.eat(cls.pop_food(microbe.cell_position, world))

    @classmethod
    def pop_food(cls, cell_position, world):
        food_matrix = world.store[FOOD]
        food = food_matrix[cell_position.y][cell_position.x].pop(0)
        world[FOOD].remove(food)
        return food

    @classmethod
    def has_food(cls, cell_position, world):
        food_matrix = world.store[FOOD]
        return len(food_matrix[cell_position.y][cell_position.x])


class Food(Drawable):
    def __init__(self, cell_position, color=Color(0, 255, 0)):
        self.cell_position = cell_position
        super().__init__(Microbe.to_actual_position(self.cell_position), Microbe.CELL_SIZE / 4, color)
        self.energy = Microbe.FOOD_ENERGY
