from random import randint


class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scaled_to(self, scale_factor):
        return Coordinate(self.x * 1 / scale_factor, self.y * 1 / scale_factor)

    @staticmethod
    def generate_random(self, max_x, max_y, used):
        x = randint(0, max_x)
        y = randint(0, max_y)
        coordinate = Coordinate(x, y)
        while coordinate in used:
            x = randint(0, max_x)
            y = randint(0, max_y)
            coordinate = Coordinate(x, y)
        return coordinate
