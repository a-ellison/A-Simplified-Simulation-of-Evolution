import logging
import time
from animal import Animal
from enum import Enum
from DNA import DNA

# Configure logging
logging.basicConfig(filename='world.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


class WorldState(Enum):
    STOP = 0
    GO = 1


class World(object):
    def __init__(self,world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

        self.all_animals = []
        self.used_positions = set()
        self.time = 0

        self.world_state = WorldState.STOP

    def start_world(self):
        logging.debug('World Started')
        self.create_test_animal((self.world_width / 2, self.world_height / 2), DNA(3, 'red'))
        self.create_test_animal((4.5, 50.5), DNA(1, 'green'))
        self.world_state = WorldState.GO

    def create_test_animal(self, coordinates, DNA):
        new_animal = Animal(*coordinates, DNA)
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
            time.sleep(3)
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
