import random

from models.beeplant.util import Direction
from models.cell_agent import CellAgent
from structs.color import Color
from structs.point import Point


class Bee(CellAgent):
    CELL_SIZE = 5
    STEP_COST = 1
    START_ENERGY = 100
    MAX_POLLEN = 20
    REPRODUCTION_ENERGY = 500
    ENERGY_PER_POLLEN = 2

    def __init__(self, cell_position, hunger):
        super().__init__(cell_position, Color(255, 239, 0))
        self.energy = self.START_ENERGY
        self.hunger = hunger
        self.direction = Direction.random()
        self.pollen = 0

    def move(self, min_cell, max_cell):
        self.cell_position = self.direction.move(self.cell_position).restrict_to(min_cell, max_cell)
        self.direction.steer(random.randint(-1, 1))
        self.update_position()
        self.energy -= Bee.STEP_COST
        self.age += 1

    def land(self, plant):
        plant.receive(self.give())
        self.pollen += plant.drop()
        self.eat()

    def eat(self):
        n = min(self.hunger, self.pollen)
        self.pollen -= n
        self.energy += self.ENERGY_PER_POLLEN * n

    def give(self):
        count = self.pollen
        self.pollen = 0
        return count

    def mutate(self):
        new_hunger = self.hunger + random.randint(-1,1)
        return Bee(self.cell_position, new_hunger)

    @classmethod
    def random(cls, min_cell, max_cell, **kwargs):
        cell_position = kwargs.get('cell_position')
        if cell_position is None:
            cell_position = Point.random(min_cell, max_cell)
        hunger = kwargs.get('hunger')
        if hunger is None:
            hunger = random.randint(1, 10)
        return Bee(cell_position, hunger)
