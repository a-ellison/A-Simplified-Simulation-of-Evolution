import random
from enum import Enum

from helpers import State
from models.microbe.behavior import MicrobeBehavior
from models.primer.behavior import PrimerBehavior
from models.world import World


class Behaviors(Enum):
    PRIMER = PrimerBehavior
    MICROBE = MicrobeBehavior


class Simulation:
    def __init__(
        self, world_width, world_height, behavior, seed, config, **data_kwargs
    ):
        self.world_width = world_width
        self.world_height = world_height
        random.seed(seed)
        self.world = World(self.world_width, self.world_height, seed, config)
        self.behavior = behavior
        self.behavior.initialize(self.world)
        self.data_collector = self.behavior.get_data_collector(
            self.world, **data_kwargs
        )

    def step(self, speed):
        if self.behavior.is_dead(self.world):
            return State.FINISHED
        duration = self.behavior.apply(self.world, speed)
        self.data_collector.collect(duration)
        self.world.time += 1
        return State.CONTINUE

    @property
    def all_drawables(self):
        return self.world.all_drawables

    def save(self):
        if self.world.time > 0:
            self.data_collector.save()

    def update_config(self, config):
        self.world.config = config
