import logging

from models import behavior
from application import data_collector
from models.world import World


class Simulation:
    ERROR = 0
    CONTINUE = 1
    FINISHED = 2

    def __init__(self, world_width, world_height, start_population, food_count):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = behavior.Behavior
        self.world = World(self.world_width, self.world_height)
        self.behavior.initialize(self.world, start_population, food_count)
        self.data_collector = data_collector.DataCollector(self.world)

    def step(self, speed, delay=0):
        if self.world.is_dead:
            return self.FINISHED
        import time
        start = time.perf_counter()
        for i in range(speed):
            self.behavior.apply(self.world)
            self.data_collector.track()
        duration = time.perf_counter() - start
        if duration < delay:
            time.sleep(delay - duration)
        return self.CONTINUE

    @property
    def all_drawables(self):
        return self.world.all_drawables

    def reset(self, start_population, food_count):
        self.world.wipe()
        self.behavior.initialize(self.world, start_population, food_count)

    def save(self):
        if self.world.time > 0:
            self.data_collector.save()
