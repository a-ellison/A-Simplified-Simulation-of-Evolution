import random

from helpers import State
from models import behavior
from application import data_collector
from models.world import World


class Simulation:
    def __init__(self, world_width, world_height, seed, start_population, food_count):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = behavior.Behavior
        random.seed(seed)
        self.world = World(self.world_width, self.world_height, seed)
        self.behavior.initialize(self.world, start_population, food_count)
        self.data_collector = data_collector.DataCollector(self.world)

    def step(self, speed):
        if self.world.is_dead:
            return State.FINISHED
        self.behavior.apply(self.world, speed)
        self.data_collector.track()
        return State.CONTINUE

    @property
    def all_drawables(self):
        return self.world.all_drawables

    def save(self):
        if self.world.time > 0:
            self.data_collector.save()
