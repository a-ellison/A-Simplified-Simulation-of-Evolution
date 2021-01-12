import json
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
import matplotlib.pyplot as plt

import threading


class DataCollector(ABC):
    def __init__(self, world, model_name, folder='data'):
        self.world = world
        now = datetime.now()
        self.name = f'{model_name}.{now.hour}h-{now.minute}m-{now.second}s'
        self.data_folder = folder
        self.folder = os.path.join(self.data_folder, self.name)
        self.performance = []
        self._saving = False

    def save(self):
        if not self._saving and self.has_data:
            x = threading.Thread(target=self._save)
            x.start()
        else:
            logging.info('No data to save')

    def _save(self):
        if os.path.isdir(self.data_folder) is False:
            os.mkdir(self.data_folder)
        if os.path.isdir(self.folder) is False:
            os.mkdir(self.folder)
        self.save_plots()
        data = {
            'seed': self.world.seed,
            'time': self.world.time
        }
        data.update(self.export_data())
        with open(f'{self.folder}/raw.json', 'w+') as json_file:
            json.dump(data, json_file)

    @property
    @abstractmethod
    def has_data(self):
        pass

    def collect(self, duration):
        self.performance.append(duration)

    def save_plots(self):
        self.plot_performance()

    def plot_performance(self):
        fig, ax = plt.subplots()
        ax.plot([i for i in range(1, len(self.performance) + 1)], self.performance)
        ax.set_title('Step duration (in s) over time')
        fig.savefig(f'{self.folder}/performance.png')
        plt.close(fig)

    @abstractmethod
    def export_data(self):
        pass
