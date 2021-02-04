import matplotlib.pyplot as plt
import numpy as np

from models.data_collector_base import DataCollector
from models.microbe.microbe import Direction


class MicrobeData(DataCollector):
    def __init__(self, world, **kwargs):
        super().__init__(world, model_name="MICROBE", **kwargs)
        self.population = [len(self.world["MICROBES"])]
        self.food_available = [len(self.world["FOOD"])]
        self.food_eaten = []
        self.food_generated = []
        self.probabilities = []
        self.average_probabilities = []
        self.average_age = []
        self.average_energy = []
        self.directions = []
        self.direction_popularity = []
        self.start_params = self.world.config.copy()

    @property
    def has_data(self):
        return True

    def export_data(self):
        data = self.start_params.copy()
        data.update(
            {
                "population": self.population,
                "food_available": self.food_available,
                "food_eaten": self.food_eaten,
                "food_generated": self.food_generated,
                "probabilities": self.probabilities,
                "average_probabilities": self.average_probabilities,
                "average_age": self.average_age,
                "directions": self.directions,
                "direction_popularity": self.direction_popularity,
            }
        )
        return data

    def collect(self, duration):
        super(MicrobeData, self).collect(duration)
        microbes = self.world["MICROBES"]
        self.population.append(len(microbes))
        self.probabilities = [m.probabilities for m in microbes]
        probability_averages = []
        for i in range(8):
            probability_averages.append(np.average([p[i] for p in self.probabilities]))
        self.average_probabilities.append(probability_averages)
        self.directions = [m.direction.value for m in microbes]
        popularity = [0 for _ in range(8)]
        for d in self.directions:
            popularity[d] += 1
        self.direction_popularity.append(popularity)
        food = self.world["FOOD"]
        food_generated = self.world.config["food_per_step"]
        self.food_eaten.append(self.food_available[-1] - (len(food) - food_generated))
        self.food_generated.append(food_generated)
        self.food_available.append(len(food))
        self.average_age.append(np.average([m.age for m in microbes]))
        self.average_energy.append(np.average([m.energy for m in microbes]))
        if self.auto_save and self.world.time % 1000 == 0:
            self.save()

    def save_plots(self):
        super(MicrobeData, self).save_plots()
        self.plot_population()
        self.plot_food()
        self.plot_probability_averages()
        self.plot_probability_distributions()
        self.plot_age_energy()
        self.plot_direction_popularity()
        self.plot_direction_distribution()

    def plot_population(self):
        fig, (ax_population, ax_food) = plt.subplots(2, 1, sharex=True)
        ax_population.plot(self.population, label="Microbes", color="blue")
        ax_population.legend()
        ax_food.plot(self.food_available, label="Bacteria", color="green")
        ax_food.legend()
        fig.suptitle("Microbe/Bacteria population over time")
        fig.savefig(f"{self.folder}/population.png")
        plt.close(fig)

    def plot_food(self):
        fig, ax = plt.subplots()
        ax.bar(
            [i for i in range(self.world.time)],
            self.food_eaten,
            color="red",
            label="Eaten",
        )
        ax.plot(
            self.food_generated,
            color="green",
            label="Generated",
        )
        ax.set_title("Food consumption over time")
        ax.legend()
        fig.savefig(f"{self.folder}/food.png")
        plt.close(fig)

    def plot_probability_averages(self):
        fig, ax = plt.subplots()
        for i in range(8):
            averages = [p[i] for p in self.average_probabilities]
            ax.plot(averages, label="$p_{%d}$" % i)
        ax.legend()
        fig.suptitle("Average probabilities over time")
        fig.savefig(f"{self.folder}/average-probabilities.png")
        plt.close(fig)

    def plot_probability_distributions(self):
        for i in range(8):
            if i % 2 == 0:
                fig, axes = plt.subplots(2, 1)
                for k in range(2):
                    ax = axes[k]
                    ax.hist(
                        [a[i + k] for a in self.probabilities],
                        label=r"$p_{%d}$" % (i + k),
                        bins="auto",
                        rwidth=0.85,
                    )
                    ax.legend()
                fig.suptitle(
                    "Distribution of probabilities $p_{%d},p_{%d}$" % (i, i + 1)
                )
                fig.savefig(f"{self.folder}/probability-distributions-p{i},{i + 1}.png")
                plt.close(fig)

    def plot_age_energy(self):
        fig, (ax_age, ax_energy) = plt.subplots(2, 1, sharex=True)
        ax_age.plot(
            self.average_age,
            label="Age",
            color="black",
        )
        ax_age.legend()
        ax_energy.plot(
            self.average_energy,
            label="Energy",
            color="blue",
        )
        ax_energy.legend()
        fig.suptitle("Average age and energy")
        fig.savefig(f"{self.folder}/age-energy.png")
        plt.close(fig)

    def plot_direction_popularity(self):
        fig, ax = plt.subplots()
        for i in range(8):
            popularity_over_time = [d[i] for d in self.direction_popularity]
            ax.plot(popularity_over_time, label=Direction(i).name)
        ax.legend()
        fig.suptitle("Direction popularity over time")
        fig.savefig(f"{self.folder}/direction-popularity.png")
        plt.close(fig)

    def plot_direction_distribution(self):
        fig, ax = plt.subplots()
        ax.hist(
            [Direction(d).name for d in self.directions],
            bins=8,
            rwidth=0.85,
        )
        fig.suptitle("Distribution of directions")
        fig.savefig(f"{self.folder}/direction-distributions.png")
        plt.close(fig)
