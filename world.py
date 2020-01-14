import logging
from random import randint
import animal
from enum import Enum
from DNA import DNA

# Configure logging
logging.basicConfig(filename='world.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


class WorldState(Enum):
    STOP = 0
    GO = 1


class World(object):
    def __init__(self, world_length):
        self.world_length = world_length

        # self.all_animals = [[None for _ in range(world_length)] for _ in range(world_length)]
        self.all_animals = []
        self.used_positions = set()
        self.time = 0
        # self.start_population =

        self.world_state = WorldState.STOP

    def start_world(self):
        logging.debug('World Started')
        self.create_test_animal((self.world_length / 2, self.world_length / 2), DNA(10, 'red'))
        self.create_test_animal((4.5, 50.5), DNA(9, 'green'))
        self.world_state = WorldState.GO

    def create_test_animal(self, coordinates, DNA):
        new_animal = animal.Animal(*coordinates, DNA)
        self.all_animals.append(new_animal)
        self.used_positions.add(coordinates)

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
