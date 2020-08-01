import logging
import time


class Simulation():
    def __init__(self, world_width, world_height):
        self.w = world_width
        self.h = world_height

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
