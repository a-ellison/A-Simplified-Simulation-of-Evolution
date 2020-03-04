import logging
from animal import Animal
from coordinate import Coordinate
from DNA import DNA
from enum import Enum

# Configure logging
logging.basicConfig(filename='world.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')

START_POPULATION = 100


class WorldState(Enum):
    STOP = 0
    GO = 1


class World(object):
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        Animal.MAX_X = self.world_width
        Animal.MAX_Y = self.world_height

        self.MIN_SIZE = DNA.calculate_min_animal_size(min(world_width, world_height))
        self.MAX_SIZE = DNA.calculate_max_animal_size(min(world_width, world_height))
        self.MIN_SPEED = DNA.calculate_min_animal_speed(min(world_width, world_height))
        self.MAX_SPEED = DNA.calculate_max_animal_speed(min(world_width, world_height))

        self.all_animals = []
        self.used_coordinates = set()
        self.time = 0

        self.world_state = WorldState.STOP

    def start_world(self):
        logging.debug('World Started')
        self.create_animal(Coordinate(20, 20), DNA(0, 'red', size=2))
        self.create_animal(Coordinate(40, 40), DNA(0, 'green', size=3))
        self.create_animal(Coordinate(60, 60), DNA(0, 'blue', size=4))
        self.create_animal(Coordinate(80, 80), DNA(0, 'orange', size=5))
        self.create_animal(Coordinate(80, 80), DNA(0, 'yellow', size=7))
        self.create_animal(Coordinate(80, 80), DNA(0, 'magenta', size=10))
        # self.generate_animals()
        self.world_state = WorldState.GO

    def generate_animals(self):
        for i in range(START_POPULATION):
            self.generate_animal()

    def generate_animal(self):
        random_coordinate = Coordinate.generate_random(self.world_width, self.world_height,
                                                       self.used_coordinates)
        random_dna = DNA.generate_random(self.MIN_SIZE, self.MAX_SIZE, self.MIN_SPEED, self.MAX_SPEED)
        self.create_animal(random_coordinate, random_dna)

    def create_animal(self, coordinate, DNA):
        new_animal = Animal(coordinate, DNA)
        self.all_animals.append(new_animal)
        self.used_coordinates.add(coordinate)

    def run(self):
        logging.debug('Run called')
        if self.world_state == WorldState.GO:
            logging.debug('Running')
            self.test_step()

    def test_step(self):
        for animal in self.all_animals:
            animal.move()
            logging.debug('Animal moved')

    # TODO: Implement mating of two animals
    def mate_animals(self, parent_1, parent_2):
        pass

    def step(self):
        self.time += 1
        for i in self.all_animals:
            pass

    def is_running(self):
        return self.world_state == WorldState.GO
