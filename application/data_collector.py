import json
import matplotlib.pyplot as plt
from datetime import datetime


# TODO: display deaths and births
from models import animal


class DataCollector(object):
    def __init__(self, world):
        self.world = world
        self.folder = 'data'
        now = datetime.now()
        self.name = f'{now.hour}h-{now.minute}m-{now.second}s'
        self.days = []
        self.population = []
        self.average_radius = []
        self.average_speed = []
        self.average_sight_range = []

    def plot_population(self):
        fig, ax = plt.subplots()
        ax.plot(self.days, self.population)
        ax.set_title('Population over time')
        fig.savefig(f'{self.folder}/{self.name}-population.png')

    def plot_traits(self):
        fig, ax = plt.subplots()
        relative_radius_average = self.relative_average(self.average_radius, animal.MAX_RADIUS)
        relative_speed_average = self.relative_average(self.average_speed, animal.MAX_SPEED)
        relative_sight_range_average = self.relative_average(self.average_sight_range, animal.MAX_SIGHT_RANGE)
        ax.plot(self.days, relative_radius_average, label='radius')
        ax.plot(self.days, relative_speed_average, label='speed')
        ax.plot(self.days, relative_sight_range_average, label='sight range')
        all_averages = relative_radius_average + relative_speed_average + relative_sight_range_average
        min_y = int(min(all_averages) / 10) * 10
        ax.set_ylim(min_y, 100)
        ax.legend()
        fig.savefig(f'{self.folder}/{self.name}-traits.png')

    @classmethod
    def relative_average(cls, averages_list, max_value):
        return [(avg / max_value) * 100 for avg in averages_list]

    def save(self):
        self.plot_population()
        self.plot_traits()
        data = {
            'time': self.world.time,
            'days': self.days,
            'population': self.population,
        }
        with open(f'{self.folder}/{self.name}.json', 'w+') as json_file:
            json.dump(data, json_file)

    def track(self):
        if self.world.is_asleep:
            self.population.append(len(self.world.all_animals))
            self.days.append(len(self.days) + 1)
            self.average_radius.append(self.average([a.radius for a in self.world.all_animals]))
            self.average_speed.append(self.average([a.speed for a in self.world.all_animals]))
            self.average_sight_range.append(self.average([a.sight_range for a in self.world.all_animals]))
            self.save()

    @classmethod
    def average(cls, numbers):
        return sum(numbers) / len(numbers)
