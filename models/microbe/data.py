import logging
import threading

from models.data_collector_base import DataCollector
import matplotlib.pyplot as plt


class MicrobeData(DataCollector):
    def __init__(self, world):
        super().__init__(world, 'MICROBE')
        self.population = []

    @property
    def has_data(self):
        return True

    def collect(self, duration):
        super(MicrobeData, self).collect(duration)
        self.population.append(len(self.world['MICROBES']))
        if self.world.time % 1000 == 0:
            self.save()

    def plot_population(self):
        fig, ax = plt.subplots()
        ax.plot([i + 1 for i in range(len(self.population))], self.population)
        ax.set_title('Population over time')
        fig.savefig(f'{self.folder}/{self.name}-population.png')
        plt.close(fig)

    def save_plots(self):
        super(MicrobeData, self).save_plots()
        self.plot_population()

    def export_data(self):
        return {
            'seed': self.world.seed,
            'population': self.population
        }
