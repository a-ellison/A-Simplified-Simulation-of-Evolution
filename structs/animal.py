from math import cos
from math import sin

from coordinate import Coordinate


class Animal(object):
    def __init__(self, coordinate, dna):
        self.x = coordinate.x
        self.y = coordinate.y
        self.dna = dna

    @classmethod
    def set_limits(cls, MAX_X, MAX_Y):
        Animal.MAX_X = MAX_X
        Animal.MAX_Y = MAX_Y

    def move(self):
        d = self.dna.get_speed()
        angle = self.dna.get_direction()
        dx = cos(angle) * d
        self.x += dx
        dy = sin(angle) * d
        self.y += dy

    def get_coordinate(self):
        return Coordinate(self.x, self.y)

    def get_color(self):
        return self.dna.color

    def get_size(self):
        return self.dna.size
