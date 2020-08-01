import logging
from time import perf_counter
from primitive_animal import PrimitiveAnimal
from point import Point
from primitvie_behavior import PrimitiveBehavior
from primitive_dna import PrimitiveDNA
from enum import Enum

START_POPULATION = 50

BEHAVIOR = PrimitiveBehavior
ANIMAL = PrimitiveAnimal
DNA = PrimitiveDNA


class World(object):
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        BEHAVIOR.set_limits(self.world_width, self.world_height)

        self.all_animals = []
        self.time = 0
        self.deaths = 0
        self.births = 0

        self.world_state = WorldState.STOP

    def initialize_world(self):
        logging.debug('World started')
        self.generate_animals()
        self.world_state = WorldState.GO

    def generate_animals(self):
        for i in range(START_POPULATION):
            self.generate_animal()

    def generate_animal(self):
        random_point = Point.random(self.world_width, self.world_height)
        random_dna = DNA.random()
        self.create_animal(random_point, random_dna)

    def create_animal(self, point, dna):
        new_animal = PrimitiveAnimal(point, dna)
        self.all_animals.append(new_animal)
        Point.insert(point)

    def run(self):
        if self.world_state == WorldState.GO:
            self.step()

    def step(self):
        self.time += 1
        for i in self.all_animals:
            i.move()

    def is_running(self):
        return self.world_state == WorldState.GO

    def get_population(self):
        return len(self.all_animals)

    # TODO: Calculate deaths after each step
    def get_deaths(self):
        return -1

    # TODO: Calculate births after each step
    def get_births(self):
        return -1

    # TODO: Keep track of number of species
    def get_species(self):
        return -1

    # TODO Implement temperature
    def get_temperature(self):
        return -1
