class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y=y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def scale(self, scale_factor):
        return Coordinate(self.x * 1/scale_factor, self.y * 1/scale_factor)

