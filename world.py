from random import randint

import animal


class World(object):
    def __init__(self, world_length):
        self.world_length = world_length
        # self.all_animals = [[None for _ in range(world_length)] for _ in range(world_length)]
        self.all_animals = []
        self.time = 0
        self.used_positions = set()

    def create_animal(self, color):
        random_coords = (randint(1, self.world_length), randint(1, self.world_length))
        while random_coords in self.used_positions:
            random_coords = (randint(1, self.world_length), randint(1, self.world_length))
        new_animal = animal.Animal(*random_coords, None, color, 0)
        self.all_animals.append(new_animal)
        self.used_positions.add(random_coords)

    def start_world(self):
        self.create_animal('red')
        self.create_animal('green')
        self.create_animal('blue')

    def step(self):
        self.time += 1
        for a in self.all_animals:
            pass
        pass

