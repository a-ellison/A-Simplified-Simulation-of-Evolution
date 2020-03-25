from random import randint
from helper_classes.functions import Functions
from color import Color

FACTOR = 100
MIN_SIZE = 150 / 100
MAX_SIZE = 240 / 100
MIN_SPEED = 150 / 100
MAX_SPEED = 240 / 100


class DNA(object):
    def __init__(self, speed: int, color: Color, size: int, direction: int, max_energy: int, sight_range: int):
        self.speed = speed
        self.color = color
        self.direction = direction  # degrees
        self.max_energy = max_energy
        self.sight_range = sight_range
        self.size = size

    @classmethod
    def merge(cls, parent1, parent2):
        pass

    @classmethod
    def random(cls):
        speed = Functions.uniform(MIN_SPEED, MAX_SPEED, FACTOR)
        color = Color.random()
        size = Functions.uniform(MIN_SIZE, MAX_SIZE, FACTOR)
        direction = randint(1, 360)
        max_energy = 99
        sight_range = 99
        return DNA(speed, color, size, direction, max_energy, sight_range)

    def get_speed(self):
        return self.speed

    def get_size(self):
        return self.speed

    def get_color(self):
        return self.color

    def get_max_energy(self):
        return self.max_energy

    def get_direction(self):
        return self.direction
