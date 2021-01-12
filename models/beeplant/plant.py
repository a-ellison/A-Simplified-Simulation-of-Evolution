import random

from models.beeplant.util import Direction
from models.cell_agent import CellAgent
from structs.color import Color
from structs.point import Point


class Plant(CellAgent):
    STEP_COST = 1
    START_ENERGY = 500

    def __init__(self, cell_position, reproduction_chance):
        super().__init__(cell_position, Color(50, 205, 50))
        self.energy = self.START_ENERGY
        self.reproduction_chance = reproduction_chance
        self.pollen = 0
        self.received_pollen = 0

    def create_pollen(self):
        self.pollen += 1
        r = random.random()
        if r < 1 - self.reproduction_chance:
            self.pollen += 1
        self.energy -= self.STEP_COST
        self.age += 1

    def try_reproduce(self, min_cell, max_cell):
        r = random.random()
        if self.received_pollen and r < self.reproduction_chance:
            return self.mutate(min_cell, max_cell)

    def drop(self):
        n = int(self.pollen / 2)
        self.pollen -= n
        return n

    def receive(self, pollen):
        self.received_pollen = pollen

    @property
    def is_alive(self):
        return self.energy > 0

    def mutate(self, min_cell, max_cell):
        delta = random.choice([-0.1, 0, 0.1])
        new_reproduction_chance = min(0.9, max(0.1, self.reproduction_chance + delta))
        new_pos = Direction.random().move(self.cell_position).restrict_to(min_cell, max_cell, True)
        return Plant(new_pos, new_reproduction_chance)

    @classmethod
    def random(cls, min_cell, max_cell, **kwargs):
        cell_position = kwargs.get('cell_position', Point.random(min_cell, max_cell))
        reproduction_chance = kwargs.get('reproduction_chance', random.random())
        return Plant(cell_position, reproduction_chance)
