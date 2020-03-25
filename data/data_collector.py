import matplotlib.pyplot as plt
import numpy as np


class DataCollector(object):
    def __init__(self, world):
        self.world = world
        self.max_t = 0
        self.dt = 1
        self.deaths = []
        self.births = []
        self.population = []
        self.species = []
        self.temperature = []

    # TODO: Implement plotting graph to window or file
    def plot_population(self, ax):
        length = int(self.max_t / self.dt)
        t = [i for i in range(length)]
        population = [self.population[i] for i in range(length) if i % self.dt == 0]
        ax.plot(t, self.population)

    # TODO: Implement saving to file
    def save(self):
        pass

    # TODO: Implement loading from file
    @classmethod
    def from_JSON(cls):
        pass

    def track(self):
        self.population.append(self.world.get_population())
        self.deaths.append(self.world.get_deaths())
        self.births.append(self.world.get_births())
        self.species.append(self.world.get_species())
        self.temperature.append(self.world.get_temperature())
