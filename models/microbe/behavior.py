import logging
import time

from helpers import Speed
from models.behavior_base import BehaviorBase
from models.drawable import Drawable
from models.microbe.data import MicrobeData
from models.microbe.microbe import Microbe
from structs.color import Color

START_MICROBE_NUM = 10
MICROBES = 'MICROBES'
START_FOOD_NUM = 100
FOOD = 'FOOD'
FOOD_PER_STEP = 2


class MicrobeBehavior(BehaviorBase):
    @classmethod
    def initialize(cls, world):
        cls.set_food_matrix(world)
        world[MICROBES] = []
        cls.generate_microbes(START_MICROBE_NUM, world)
        world[FOOD] = []
        cls.generate_food(START_FOOD_NUM, world)

    @classmethod
    def generate_microbes(cls, n, world):
        for i in range(START_MICROBE_NUM):
            m = cls.generate_microbe(world)
            world[MICROBES].append(m)

    @classmethod
    def generate_microbe(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        return Microbe.random(min_cell, max_cell)

    @classmethod
    def to_cell_corners(cls, min_coordinate, max_coordinate):
        min_cell = min_coordinate.translate(1 / Microbe.CELL_SIZE).to_integers()
        max_cell = max_coordinate.translate(1 / Microbe.CELL_SIZE).move_by(-1).to_integers()
        return min_cell, max_cell

    @classmethod
    def generate_food(cls, n, world):
        food_matrix = world.store[FOOD]
        for i in range(n):
            f = cls.generate_single_food(world)
            world[FOOD].append(f)
            food_matrix[f.cell_position.y][f.cell_position.x].append(f)

    @classmethod
    def generate_single_food(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        cell_position = Microbe.random_position(min_cell, max_cell)
        return Food(cell_position)

    @classmethod
    def set_food_matrix(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        food_matrix = [[[] for i in range(min_cell.x, max_cell.x + 1)] for k in range(min_cell.y, max_cell.y + 1)]
        world.store[FOOD] = food_matrix

    @classmethod
    def get_data_collector(cls, world):
        return MicrobeData(world)

    @classmethod
    def apply(cls, world, speed):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        start = time.perf_counter()
        cls.generate_food(FOOD_PER_STEP, world)
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
        n = len(world[MICROBES])
        logging.info(f'there are {n} microbes')
        logging.info(f'average microbe energy is {sum([m.energy for m in world[MICROBES]])/n}')
        delay = 0.5 if speed == Speed.SLOW else 0
        if duration < delay:
            time.sleep(delay - duration)
        return duration

    @classmethod
    def is_dead(cls, world):
        return False

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
