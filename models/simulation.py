import logging
import time

from models import world
from models.primitive.primitive_behavior import PrimitiveBehavior


class Simulation:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = PrimitiveBehavior
        self.world = world.World(self.behavior.ANIMAL, self.world_width, self.world_height)
        self.behavior.initialize(world)

    # TODO: Implement loading world file
    def load(self, world_data):
        raise NotImplementedError

    # TODO: Implement saving to file
    def save(self):
        raise NotImplementedError

    def step(self):
        logging.info('step started')
        time.sleep(3)
        logging.info('step done')

    def get_all_objects(self):
        return self.world.all_objects
