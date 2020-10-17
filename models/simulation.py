import logging

from models import world
from models.primitive.primitive_behavior import PrimitiveBehavior


class Simulation:
    def __init__(self, world_width, world_height, start_population, food_count):
        self.world_width = world_width
        self.world_height = world_height
        self.behavior = PrimitiveBehavior
        self.world = world.World(self.world_width, self.world_height)
        self.behavior.initialize(self.world, start_population, food_count)

    # TODO: Implement loading world file
    def load(self, world_data):
        raise NotImplementedError

    # TODO: Implement saving to file
    def save(self):
        raise NotImplementedError

    def step(self, speed):
        try:
            import time
            start = time.perf_counter()
            for i in range(speed):
                self.behavior.apply(self.world)
            duration = time.perf_counter() - start
            # if duration < 0.1:
            #     time.sleep(0.1 - duration)
            return True
        except BaseException as e:
            logging.error(str(e))
            return False

    @property
    def all_drawables(self):
        return self.world.all_drawables

    def reset(self, start_population, food_count):
        self.world.wipe()
        self.behavior.initialize(self.world, start_population, food_count)
