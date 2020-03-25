import logging
from time import perf_counter
from structs.animal import Animal
from coordinate import Coordinate
from dna import DNA
from enum import Enum

START_POPULATION = 50


class WorldState(Enum):
    STOP = 0
    GO = 1


class World(object):
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        Animal.set_limits(self.world_width, self.world_height)

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
        random_coordinate = Coordinate.random(self.world_width, self.world_height)
        random_dna = DNA.random()
        self.create_animal(random_coordinate, random_dna)

    def create_animal(self, coordinate, dna):
        new_animal = Animal(coordinate, dna)
        self.all_animals.append(new_animal)
        Coordinate.insert(coordinate)

    def run(self):
        logging.debug('Run called')
        if self.world_state == WorldState.GO:
            self.step()

    def step(self):
        self.time += 1
        for i in self.all_animals:
            t = perf_counter()
            i.move()
            logging.debug(f'Animal moved t: {perf_counter() - t}')

    # TODO: Implement mating
    def mate_animals(self, parent_1, parent_2):
        pass

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

