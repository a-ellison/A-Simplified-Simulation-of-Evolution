from coordinates import Coordinate


class Animal(object):
    def __init__(self, start_x, start_y, DNA):
        self.x = start_x
        self.y = start_y
        self.DNA = DNA

    def move(self):
        self.x += self.DNA.speed

    def get_coordinate(self):
        return Coordinate(self.x, self.y)

    def get_color(self):
        return self.DNA.color
