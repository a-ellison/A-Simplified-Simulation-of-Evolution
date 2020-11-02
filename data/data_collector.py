import csv
import math


class DataCollector(object):
    def __init__(self, world):
        self.world = world
        self.max_t = 0
        self.dt = 1
        self.deaths = []
        self.births = []
        self.population = []
        self.average_distances = []
        # self.temperature = []

    # TODO: Implement plotting graph to window or file
    def plot_population(self, ax):
        length = int(self.max_t / self.dt)
        t = [i for i in range(length)]
        population = [self.population[i] for i in range(length) if i % self.dt == 0]
        ax.plot(t, self.population)

    # TODO: Implement saving to file
    def save(self):
        pass

    def save_test(self):
        with open('test.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow([i for i in range(self.world.time)])
            writer.writerow([i for i in self.average_distances])

    # TODO: Implement loading from file
    @classmethod
    def from_JSON(cls):
        pass

    def track(self):
        return
        total = 0
        for a in self.world.all_animals:
            if not a.has_moved:
                break
            else:
                dx = a.x - a.last_x
                dy = a.y - a.last_y
                total += math.sqrt(dx ** 2 + dy ** 2)
        self.average_distances.append(total / len(self.world.all_animals))
