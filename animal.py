from coordinates import Coordinate


class Animal(object):
    def __init__(self, coordinate, dna):
        self.x = coordinate.x
        self.y = coordinate.y
        self.dna = dna

    def move(self):
        self.x += self.dna.speed

    def get_coordinate(self):
        return Coordinate(self.x, self.y)

    def get_color(self):
        return self.dna.color

    def get_size(self):
        return self.dna.size
