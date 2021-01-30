import matplotlib.pyplot as plt
import numpy as np

from models.data_collector_base import DataCollector
from models.primer.animal import PrimerAnimal


class PrimerData(DataCollector):
    def __init__(self, world, **kwargs):
        super().__init__(world, model_name="PRIMER", **kwargs)
        self.days = []
        self.population = []
        self.radius_color = "red"
        self.radii = []
        self.radius_average = []
        self.radius_deviation = []
        self.speed_color = "green"
        self.speeds = []
        self.speed_average = []
        self.speed_deviation = []
        self.sight_range_color = "blue"
        self.sight_ranges = []
        self.sight_range_average = []
        self.sight_range_deviation = []
        self.known_ids = []
        self.food_generated = [self.world.config["food_count"]]
        self.food_eaten = []
        self.average_age = []
        self.start_params = self.world.config.copy()
        animals = self.world["ANIMALS"]
        self.population.append(len(animals))
        self.collect_traits(animals)

    def plot_population(self):
        fig, ax = plt.subplots()
        ax.plot(
            [i for i in range(len(self.days) + 1)],
            self.population,
            label="Population",
        )
        ax.set_title("Population over time")
        fig.savefig(f"{self.folder}/population.png")
        ax.legend()
        plt.close(fig)

    def plot_traits(self):
        fig, ax = plt.subplots()
        self.ax_plot_trait(
            ax,
            self.radius_average,
            PrimerAnimal.MIN_RADIUS,
            PrimerAnimal.MAX_RADIUS,
            "radius",
            self.radius_color,
        )
        self.ax_plot_trait(
            ax,
            self.speed_average,
            PrimerAnimal.MIN_SPEED,
            PrimerAnimal.MAX_SPEED,
            "speed",
            self.speed_color,
        )
        self.ax_plot_trait(
            ax,
            self.sight_range_average,
            PrimerAnimal.MIN_SIGHT_RANGE,
            PrimerAnimal.MAX_SIGHT_RANGE,
            "sight range",
            self.sight_range_color,
        )
        ax.legend()
        ax.set_title("Average trait values (in % of min and max values)")
        fig.savefig(f"{self.folder}/traits.png")
        plt.close(fig)

    def ax_plot_trait(self, ax, averages, min_value, max_value, label, color):
        relative_average = self.values_to_percent(averages, min_value, max_value)
        days = [i for i in range(len(self.days) + 1)]
        ax.plot(days, relative_average, label=label, color=color)

    @classmethod
    def to_percent(cls, value, min_value, max_value):
        return ((value - min_value) / (max_value - min_value)) * 100

    @classmethod
    def values_to_percent(cls, values, min_value, max_value):
        return [cls.to_percent(val, min_value, max_value) for val in values]

    def plot_distributions(self):
        fig, (ax_radius, ax_speed, ax_sight_range) = plt.subplots(3, 1)
        ax_radius.hist(
            self.values_to_percent(
                self.radii, PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS
            ),
            label="radius",
            bins="auto",
            color=self.radius_color,
            rwidth=0.85,
        )
        ax_speed.hist(
            self.values_to_percent(
                self.speeds, PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED
            ),
            label="speed",
            bins="auto",
            color=self.speed_color,
            rwidth=0.85,
        )
        ax_sight_range.hist(
            self.values_to_percent(
                self.sight_ranges,
                PrimerAnimal.MIN_SIGHT_RANGE,
                PrimerAnimal.MAX_SIGHT_RANGE,
            ),
            label="sight range",
            bins="auto",
            color=self.sight_range_color,
            rwidth=0.85,
        )
        ax_radius.set_title("Distribution of traits (in % of min and max values)")
        for ax in (ax_radius, ax_speed, ax_sight_range):
            ax.legend()
        fig.savefig(f"{self.folder}/trait-distributions.png")
        plt.close(fig)

    def plot_food(self):
        fig, ax = plt.subplots()
        x = [i for i in range(1, len(self.days) + 1)]
        ax.plot(
            x,
            self.food_generated[:-1],
            color="green",
            label="Available",
        )
        ax.fill_between(x, self.food_generated[:-1], color="green")
        ax.plot(
            x,
            self.food_eaten,
            color="red",
            label="Eaten",
        )
        ax.fill_between(x, self.food_eaten, color="red")
        ax.set_title("Food consumption over time")
        ax.legend()
        fig.savefig(f"{self.folder}/food.png")
        plt.close(fig)

    def plot_age(self):
        fig, ax = plt.subplots()
        ax.plot(
            [i for i in range(1, len(self.days) + 1)],
            self.average_age,
            color="black",
        )
        ax.set_title("Average age")
        fig.savefig(f"{self.folder}/age.png")
        plt.close(fig)

    @property
    def has_data(self):
        return len(self.days)

    def save_plots(self):
        # super(PrimerData, self).save_plots()
        self.plot_traits()
        self.plot_distributions()
        self.plot_population()
        self.plot_food()
        self.plot_age()

    def export_data(self):
        data = self.start_params.copy()
        data.update(
            {
                "days": self.days,
                "population": self.population,
                "average_radius": self.radius_average,
                "average_speed": self.speed_average,
                "average_sight_range": self.sight_range_average,
                "radii": self.radii,
                "speeds": self.speeds,
                "sight_ranges": self.sight_ranges,
                "food_generated": self.food_generated,
                "food_eaten": self.food_eaten,
            }
        )
        return data

    def collect(self, duration, is_start=False):
        super(PrimerData, self).collect(duration)
        animals = self.world["ANIMALS"]
        if all([a.is_asleep for a in animals]):
            self.population.append(len(animals))
            self.days.append(self.world.time)
            self.collect_traits(animals)
            # collect happens after food is regenerated so special logic needed
            food_eaten = self.food_generated[-1] - len(self.world["FOOD"])
            self.food_eaten.append(food_eaten)
            self.food_generated.append(self.world.config["food_count"])
            self.average_age.append(np.average([a.age for a in animals]))
            if self.auto_save and len(self.days) % 25 == 0:
                self.save()

    def collect_traits(self, animals):
        self.radii = [a.radius for a in animals]
        self.radius_average.append(np.average(self.radii))
        self.radius_deviation.append(np.std(self.radii))
        self.speeds = [a.speed for a in animals]
        self.speed_average.append(np.average(self.speeds))
        self.speed_deviation.append(np.std(self.speeds))
        self.sight_ranges = [a.sight_range for a in animals]
        self.sight_range_average.append(np.average(self.sight_ranges))
        self.sight_range_deviation.append(np.std(self.sight_ranges))
