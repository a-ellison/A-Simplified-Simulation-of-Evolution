import logging

from models import behavior
from data import data_collector
from models.world import World


class Simulation:
    def __init__(self, world_width, world_height, start_population, food_count):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = behavior.Behavior
        self.world = World(self.world_width, self.world_height)
        self.behavior.initialize(self.world, start_population, food_count)
        self.data_collector = data_collector.DataCollector(self.world)

    def step(self, speed):
        try:
            import time
            start = time.perf_counter()
            for i in range(speed):
                self.behavior.apply(self.world)
                self.data_collector.track()
            duration = time.perf_counter() - start
            if duration < 0.01:
                time.sleep(0.1 - duration)
            return True
        except Exception as e:
            logging.error(str(e))
            return False

    @property
    def all_drawables(self):
        return self.world.all_drawables

    def reset(self, start_population, food_count):
        self.world.wipe()
        self.behavior.initialize(self.world, start_population, food_count)

    def save(self):
        self.data_collector.save_test()
