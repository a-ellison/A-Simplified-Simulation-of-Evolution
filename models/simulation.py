import logging
import time

from models import world
from models.primitive.primitive_behavior import PrimitiveBehavior


class Simulation:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = PrimitiveBehavior
        self.world = world.World(self.world_width, self.world_height)
        self.behavior.initialize(self.world)

    # TODO: Implement loading world file
    def load(self, world_data):
        raise NotImplementedError

    # TODO: Implement saving to file
    def save(self):
        raise NotImplementedError

    def step(self):
        self.behavior.apply(self.world)

    def get_all_drawables(self):
        return self.world.all_drawables
