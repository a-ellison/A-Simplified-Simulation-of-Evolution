import matplotlib.pyplot as plt

from models.data_collector_base import DataCollector
from models.primer.animal import PrimerAnimal

# avoid circular import
import models.primer.behavior as behavior


class PrimerData(DataCollector):
    def __init__(self, world):
        super().__init__(world, "PRIMER")
        self.days = []
        self.population = []
        self.average_radius = []
        self.average_speed = []
        self.average_sight_range = []
        self.known_ids = []
        self.births = []
        self.deaths = []
        self.last_food_generated = self.world.config["food_count"]
        self.food_eaten = []
        self.food_left = []
        self.average_age = []
        self.start_params = {
            "start_population": world.config["start_population"],
            "species": world.config["species"],
        }

    def plot_population(self):
        fig, ax = plt.subplots()
        ax.bar(
            [i for i in range(1, len(self.days) + 1)],
            self.births,
            color="green",
            label="Births",
            width=0.9,
        )
        ax.bar(
            [i for i in range(1, len(self.days) + 1)],
            [-i for i in self.deaths],
            color="red",
            label="Deaths",
            width=0.9,
        )
        ax.plot(
            [i for i in range(1, len(self.days) + 1)],
            self.population,
            label="Population",
        )
        ax.set_title("Population over time")
        fig.savefig(f"{self.folder}/population.png")
        ax.legend()
        plt.close(fig)

    def plot_traits(self):
        fig, ax = plt.subplots()
        relative_radius_average = self.relative_average(
            self.average_radius, PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS
        )
        relative_speed_average = self.relative_average(
            self.average_speed, PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED
        )
        relative_sight_range_average = self.relative_average(
            self.average_sight_range,
            PrimerAnimal.MIN_SIGHT_RANGE,
            PrimerAnimal.MAX_SIGHT_RANGE,
        )
        days = [i for i in range(1, len(self.days) + 1)]
        ax.plot(days, relative_radius_average, label="radius")
        ax.plot(days, relative_speed_average, label="speed")
        ax.plot(days, relative_sight_range_average, label="sight range")

        all_averages = (
            relative_radius_average
            + relative_speed_average
            + relative_sight_range_average
        )
        min_y = int(min(all_averages) / 10) * 10
        ax.set_ylim(min_y, 100)
        ax.legend()
        fig.savefig(f"{self.folder}/traits.png")
        plt.close(fig)

    def plot_food(self):
        fig, ax = plt.subplots()
        ax.fill(
            [i for i in range(1, len(self.days) + 1)],
            [
                self.food_eaten[i] + self.food_left[i]
                for i in range(len(self.food_eaten))
            ],
            color="blue",
            label="Eaten",
        )
        ax.fill(
            [i for i in range(1, len(self.days) + 1)],
            self.food_eaten,
            color="green",
            label="Eaten",
        )
        ax.fill(
            [i for i in range(1, len(self.days) + 1)],
            self.food_left,
            color="red",
            label="Not Eaten",
        )
        ax.set_title("Population over time")
        fig.savefig(f"{self.folder}/food.png")
        ax.legend()
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

    @classmethod
    def relative_average(cls, averages_list, min_value, max_value):
        return [
            ((avg - min_value) / (max_value - min_value)) * 100 for avg in averages_list
        ]

    @property
    def has_data(self):
        return len(self.days)

    def save_plots(self):
        # super(PrimerData, self).save_plots()
        self.plot_traits()
        self.plot_population()
        self.plot_food()
        self.plot_age()

    def export_data(self):
        data = self.start_params.copy()
        data.update(
            {
                "days": self.days,
                "population": self.population,
            }
        )
        return data

    def collect(self, duration):
        super(PrimerData, self).collect(duration)
        all_animals = behavior.PrimerBehavior.all_animals(self.world)
        if behavior.PrimerBehavior.is_asleep(
            self.world
        ) and not behavior.PrimerBehavior.is_dead(self.world):
            self.population.append(len(all_animals))
            self.days.append(self.world.time)
            self.average_radius.append(self.average([a.radius for a in all_animals]))
            self.average_speed.append(self.average([a.speed for a in all_animals]))
            self.average_sight_range.append(
                self.average([a.sight_range for a in all_animals])
            )
            self.collect_births(all_animals)
            self.last_food_generated = self.world.config["food_count"]
            food_eaten = self.last_food_generated - len(self.known_ids)
            self.food_eaten.append(food_eaten)
            self.food_left.append(self.last_food_generated - food_eaten)
            self.average_age.append(self.average([a.age for a in all_animals]))
            if len(self.days) % 50 == 0:
                self.save()

    def collect_births(self, all_animals):
        ids = [a.canvas_id for a in all_animals]
        births = 0
        for id in ids:
            try:
                i = self.known_ids.index(id)
                del self.known_ids[i]
            except ValueError:
                births += 1
        self.births.append(births)
        self.deaths.append(len(self.known_ids))
        self.known_ids = ids

    @classmethod
    def average(cls, numbers):
        return sum(numbers) / len(numbers)
