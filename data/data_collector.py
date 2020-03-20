import matplotlib.pyplot as plt
import numpy as np


class DataCollector(object):
    def __init__(self, world):
        self.world = world
        self.max_t = 0
        self.dt = 1
        self.population_decrease = []
        self.population_growth = []
        self.population_count = []
        self.species = []
        self.temperature = []

    def collect(self):
        pass

    def plot_population_count(self, ax):
        length = int(self.max_t/self.dt)
        t = [i for i in range(length)]
        population_count = [self.population_count[i] for i in range(length) if i % self.dt == 0]
        ax.plot(t, self.population_count)


    def save(self):
        pass

    @classmethod
    def from_JSON(cls):
        pass
