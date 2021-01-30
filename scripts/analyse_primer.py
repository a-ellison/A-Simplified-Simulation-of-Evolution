import json
import numpy as np
import matplotlib.pyplot as plt

from models.primer.animal import PrimerAnimal
from models.primer.data import PrimerData

file = "../useful_data/sight_needed_1000_2/raw.json"


def show_standard_deviation(data):
    for trait, min_value, max_value in (
        ("radii", PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS),
        ("speeds", PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED),
        ("sight_ranges", PrimerAnimal.MIN_SIGHT_RANGE, PrimerAnimal.MAX_SIGHT_RANGE),
    ):
        trait_data = data[trait]
        relative = PrimerData.values_to_percent(trait_data, min_value, max_value)
        print(f"Standard deviation for {trait}: {np.std(relative)}")


def show_population(data):
    days = [i for i in range(700, 980)]
    population = data["population"][700:980]
    plt.plot(days, population, label="Population")
    plt.title("Population between days 700 and 980")
    plt.legend()
    plt.show()


def show_traits(data):
    days = [i for i in range(700, 980)]
    relative_average_radius = PrimerData.values_to_percent(
        data["average_radius"], PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS
    )
    plt.plot(days, relative_average_radius[700:980], label="radius", color="red")
    relative_average_speed = PrimerData.values_to_percent(
        data["average_speed"], PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED
    )
    plt.plot(days, relative_average_speed[700:980], label="speed", color="green")
    relative_average_sight = PrimerData.values_to_percent(
        data["average_sight_range"],
        PrimerAnimal.MIN_SIGHT_RANGE,
        PrimerAnimal.MAX_SIGHT_RANGE,
    )
    plt.plot(days, relative_average_sight[700:980], label="sight range", color="blue")
    plt.legend()
    plt.title("Average trait values (in % of min and max values)")
    plt.show()


def show_filtered_distributions(data):
    fig, (ax_radius, ax_speed, ax_sight_range) = plt.subplots(3, 1)
    relative_radii = (
        PrimerData.values_to_percent(
            data["radii"], PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS
        ),
    )
    relative_speeds = (
        PrimerData.values_to_percent(
            data["speeds"], PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED
        ),
    )
    relative_sight_ranges = (
        PrimerData.values_to_percent(
            data["sight_ranges"],
            PrimerAnimal.MIN_SIGHT_RANGE,
            PrimerAnimal.MAX_SIGHT_RANGE,
        ),
    )
    selected_relative_radii = []
    selected_relative_speeds = []
    selected_relative_sight_ranges = []
    for radius, speed, sight_range in zip(
        relative_radii[0], relative_speeds[0], relative_sight_ranges[0]
    ):
        if 35 < speed < 50:
            selected_relative_radii.append(radius)
            selected_relative_speeds.append(speed)
            selected_relative_sight_ranges.append(sight_range)

    ax_radius.hist(
        selected_relative_radii,
        label="radius",
        bins="auto",
        color="red",
        rwidth=0.85,
    )
    ax_speed.hist(
        selected_relative_speeds,
        label="speed",
        bins="auto",
        color="green",
        rwidth=0.85,
    )
    ax_sight_range.hist(
        selected_relative_sight_ranges,
        label="sight range",
        bins="auto",
        color="blue",
        rwidth=0.85,
    )
    ax_radius.set_title("Distribution of traits (in % of min and max values)")
    for ax in (ax_radius, ax_speed, ax_sight_range):
        ax.legend()
    plt.show()


def show_food(data):
    days = [i for i in range(700, 980)]
    plt.plot(
        days,
        data["food_generated"][700:980],
        color="green",
        label="Available",
    )
    plt.fill_between(days, data["food_generated"][700:980], color="green")
    plt.plot(
        days,
        data["food_eaten"][700:980],
        color="red",
        label="Eaten",
    )
    plt.fill_between(days, data["food_eaten"][700:980], color="red")
    plt.title("Food consumption over time")
    plt.legend()
    plt.show()


def show_days_over_time(data):
    days = [i for i in range(700, 980)]
    plt.plot(
        days,
        data["food_generated"][700:980],
        color="green",
        label="Available",
    )
    plt.fill_between(days, data["food_generated"][700:980], color="green")
    plt.plot(
        days,
        data["food_eaten"][700:980],
        color="red",
        label="Eaten",
    )
    plt.fill_between(days, data["food_eaten"][700:980], color="red")
    plt.title("Food consumption over time")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    with open(file, "r") as raw:
        data = json.load(raw)
    show_filtered_distributions(data)
