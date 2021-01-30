import matplotlib.pyplot as plt
import numpy as np

from models.data_collector_base import DataCollector


class MicrobeData(DataCollector):
    def __init__(self, world, **kwargs):
        super().__init__(world, model_name="MICROBE", **kwargs)
        self.population = [len(self.world["MICROBES"])]
        self.probabilities = []
        self.food_available = [len(self.world["FOOD"])]
        self.food_eaten = []
        self.food_generated = []
        self.start_params = self.world.config.copy()

    @property
    def has_data(self):
        return True

    def collect(self, duration):
        super(MicrobeData, self).collect(duration)
        microbes = self.world["MICROBES"]
        self.population.append(len(microbes))
        self.probabilities.append([m.probabilities for m in microbes])
        food = self.world["FOOD"]
        food_generated = self.world.config["food_per_step"]
        self.food_eaten.append(self.food_available[-1] - (len(food) - food_generated))
        self.food_generated.append(food_generated)
        self.food_available.append(len(food))
        if self.auto_save and self.world.time % 1000 == 0:
            self.save()

    def plot_population(self):
        fig, (ax_population, ax_food) = plt.subplots(2, 1)
        x = [i for i in range(self.world.time + 1)]
        ax_population.plot(x, self.population, label="Microbes", color="blue")
        ax_population.legend()
        ax_food.plot(x, self.food_available, label="Bacteria", color="green")
        ax_food.legend()
        fig.suptitle("Microbe/Bacteria population over time")
        fig.savefig(f"{self.folder}/population.png")
        plt.close(fig)

    def plot_averages(self):
        fig, ax = plt.subplots()
        x = [i for i in range(self.world.time)]
        all_average_probabilities = []
        for a in self.probabilities:
            average_probabilities = []
            for i in range(8):
                average_probabilities.append(np.average([p[i] for p in a]))
            all_average_probabilities.append(average_probabilities)
        for i in range(8):
            average_probabilities = [p[i] for p in all_average_probabilities]
            ax.plot(x, average_probabilities, label="$p_{%d}$" % i)
        ax.legend()
        fig.suptitle("Average probabilities over time")
        fig.savefig(f"{self.folder}/average-probabilities.png")
        plt.close(fig)

    def plot_distributions(self):
        for i in range(8):
            if i % 2 == 0:
                fig, axes = plt.subplots(2, 1)
                for k in range(2):
                    ax = axes[k]
                    ax.hist(
                        [a[i + k] for a in self.probabilities[-1]],
                        label=r"$p_{%d}$" % (i + k),
                        bins="auto",
                        # color="blue",
                        rwidth=0.85,
                    )
                    ax.legend()
                fig.suptitle(
                    "Distribution of probabilities $p_{%d},p_{%d}$" % (i, i + 1)
                )
                fig.savefig(f"{self.folder}/probability-distributions-p{i},{i + 1}.png")
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
            [i for i in range(1, self.world.time + 1)],
            self.food_generated,
            color="green",
            label="Generated",
        )
        ax.set_title("Food consumption over time")
        ax.legend()
        fig.savefig(f"{self.folder}/food.png")
        plt.close(fig)

    def save_plots(self):
        # super(MicrobeData, self).save_plots()
        self.plot_population()
        self.plot_distributions()
        self.plot_food()
        self.plot_averages()

    def export_data(self):
        data = {
            "population": self.population,
            "food_available": self.food_available,
            "food_eaten": self.food_eaten,
            "food_generated": self.food_generated,
            "probabilities": self.probabilities,
        }
        data.update(self.start_params)
        return data
