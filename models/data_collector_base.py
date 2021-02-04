import json
import logging
import os
import threading
import traceback
from abc import ABC, abstractmethod
from datetime import datetime

import matplotlib.pyplot as plt


class DataCollector(ABC):
    def __init__(self, world, **kwargs):
        self.world = world
        now = datetime.now()
        self.data_folder = kwargs.get("data_folder", "data")
        self.name = f"{kwargs.get('model_name', 'MODEL')}.{now.hour}h-{now.minute}m-{now.second}s"
        self.folder = os.path.join(self.data_folder, self.name)
        self.should_save_plots = kwargs.get("save_plots", True)
        self.auto_save = kwargs.get("auto_save", True)
        self.performance = []
        self._saving = False

    @property
    @abstractmethod
    def has_data(self):
        pass

    @abstractmethod
    def export_data(self):
        pass

    def collect(self, duration):
        self.performance.append(duration)

    def save_plots(self):
        self.plot_performance()

    def plot_performance(self):
        fig, ax = plt.subplots()
        ax.plot(self.performance)
        ax.set_title("Step duration (in s) over time")
        fig.savefig(f"{self.folder}/performance.png")
        plt.close(fig)

    def save(self):
        if self._saving:
            logging.info("Busy saving")
        elif not self.has_data:
            logging.info("No data to save")
        else:
            x = threading.Thread(target=self._save)
            x.start()

    def _save(self):
        self._saving = True
        if os.path.isdir(self.data_folder) is False:
            os.mkdir(self.data_folder)
        if os.path.isdir(self.folder) is False:
            os.mkdir(self.folder)
        try:
            data = {"seed": self.world.seed, "time": self.world.time}
            data.update(self.export_data())
            with open(f"{self.folder}/raw.json", "w+") as json_file:
                json.dump(data, json_file)
            if self.should_save_plots:
                self.save_plots()
            logging.info("Data saved")
        except Exception:
            logging.error(f"Saving failed\n{traceback.format_exc()}")
        finally:
            self._saving = False
