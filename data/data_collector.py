import csv
import math
import json
from datetime import datetime


# TODO: display deaths and births
class DataCollector(object):
    def __init__(self, world):
        self.world = world
        self.days = []
        self.population = []

    # TODO: Implement plotting graph to window or file
    def plot_population(self, ax):
        length = int(self.max_t / self.dt)
        t = [i for i in range(length)]
        population = [self.population[i] for i in range(length) if i % self.dt == 0]
        ax.plot(t, self.population)

    # TODO: Implement saving to file
    def save(self):
        data = {
            'time': self.world.time,
            'days': self.days,
            'population': self.population,
        }
        now = datetime.now()
        filename = f'{now.hour}h-{now.minute}m-{now.second}s.json'
        with open(filename, 'w+') as json_file:
            json.dump(data, json_file)

    def track(self):
        self.population.append(len(self.world.all_animals))
        if self.world.is_asleep:
            self.days.append(self.world.time)
