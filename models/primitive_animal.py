from math import cos
from math import sin

from point import Point


class PrimitiveAnimal(object):
    def __init__(self, point, dna):
        self.x = point.x
        self.y = point.y
        self.dna = dna

    @classmethod
    def set_limits(cls, MAX_X, MAX_Y):
        PrimitiveAnimal.MAX_X = MAX_X
        PrimitiveAnimal.MAX_Y = MAX_Y

    def move(self):
        distance = self.dna.speed
        angle = self.dna.direction
        dx = cos(angle) * distance
        self.x += dx
        dy = sin(angle) * distance
        self.y += dy

    def get_position(self):
        return Point(self.x, self.y)

    def get_color(self):
        return self.dna.color

    def get_size(self):
        return self.dna.size
