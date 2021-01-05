import matplotlib.pyplot as plt

from models.data_collector_base import DataCollector
from models.primer.animal import PrimerAnimal
# avoid circular import
import models.primer.behavior as behavior


# TODO: display deaths and births
class PrimerData(DataCollector):
    def __init__(self, world):
        super().__init__(world, 'PRIMER')
        self.days = []
        self.population = []
        self.average_radius = []
        self.average_speed = []
        self.average_sight_range = []

    def plot_population(self):
        fig, ax = plt.subplots()
        ax.plot([i for i in range(1, len(self.days) + 1)], self.population)
        ax.set_title('Population over time')
        fig.savefig(f'{self.folder}/{self.name}-population.png')
        plt.close(fig)

    def plot_traits(self):
        fig, ax = plt.subplots()
        relative_radius_average = self.relative_average(self.average_radius, PrimerAnimal.MIN_RADIUS,
                                                        PrimerAnimal.MAX_RADIUS)
        relative_speed_average = self.relative_average(self.average_speed, PrimerAnimal.MIN_SPEED,
                                                       PrimerAnimal.MAX_SPEED)
        relative_sight_range_average = self.relative_average(self.average_sight_range, PrimerAnimal.MIN_SIGHT_RANGE,
                                                             PrimerAnimal.MAX_SIGHT_RANGE)
        days = [i for i in range(1, len(self.days) + 1)]
        ax.plot(days, relative_radius_average, label='radius')
        ax.plot(days, relative_speed_average, label='speed')
        ax.plot(days, relative_sight_range_average, label='sight range')
        all_averages = relative_radius_average + relative_speed_average + relative_sight_range_average
        min_y = int(min(all_averages) / 10) * 10
        ax.set_ylim(min_y, 100)
        ax.legend()
        fig.savefig(f'{self.folder}/{self.name}-traits.png')
        plt.close(fig)

    @classmethod
    def relative_average(cls, averages_list, min_value, max_value):
        return [((avg - min_value) / (max_value - min_value)) * 100 for avg in averages_list]

    @property
    def has_data(self):
        return len(self.days)

    def save_plots(self):
        super(PrimerData, self).save_plots()
        self.plot_traits()
        self.plot_population()

    def export_data(self):
        return {
            'days': self.days,
            'population': self.population,
        }

    def collect(self, duration):
        super(PrimerData, self).collect(duration)
        all_animals = behavior.PrimerBehavior.all_animals(self.world)
        if behavior.PrimerBehavior.is_asleep(self.world) and not behavior.PrimerBehavior.is_dead(self.world):
            self.population.append(len(all_animals))
            self.days.append(self.world.time)
            self.average_radius.append(self.average([a.radius for a in all_animals]))
            self.average_speed.append(self.average([a.speed for a in all_animals]))
            self.average_sight_range.append(self.average([a.sight_range for a in all_animals]))
            self.save()

    @classmethod
    def average(cls, numbers):
        return sum(numbers) / len(numbers)
