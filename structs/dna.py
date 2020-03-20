from random import randint
from helper_structs.color import Color

RELATIVE_MIN_ANIMAL_SIZE = 0.5  # percent of the width/height, corresponds to 2px with 360px wide/high map
RELATIVE_MAX_ANIMAL_SIZE = 2.8  # percent of the width/height, corresponds to 10px with 360px wide/high map
RELATIVE_MIN_ANIMAL_SPEED = 0.3  # percent of the width/height, corresponds to 1 px distance with 360px wide/high map
RELATIVE_MAX_ANIMAL_SPEED = 1.4  # percent of the width/height, corresponds to 5 px distance with 360px wide/high map


class DNA(object):
    def __init__(self, speed, color, energy_capacity=0, sight_range=0, size=10):
        self.speed = speed
        self.color = color
        self.energy_capacity = energy_capacity
        self.sight_range = sight_range
        self.size = size

    @classmethod
    def merge(cls, parent1, parent2):
        pass

    @classmethod
    def generate_random(cls, min_animal_size, max_animal_size, min_speed, max_speed):
        speed = randint(min_speed, max_speed)
        color = Color.generate_random()

    @classmethod
    def calculate_min_animal_size(cls, world_length):
        return round(world_length * RELATIVE_MIN_ANIMAL_SIZE)

    @classmethod
    def calculate_max_animal_size(cls, world_length):
        return round(world_length * RELATIVE_MAX_ANIMAL_SIZE)

    @classmethod
    def calculate_min_animal_speed(cls, world_length):
        return round(world_length * RELATIVE_MIN_ANIMAL_SPEED)

    @classmethod
    def calculate_max_animal_speed(cls, world_length):
        return round(world_length * RELATIVE_MAX_ANIMAL_SPEED)
