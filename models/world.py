from structs.point import Point
from models.drawable import Drawable


class World:
    def __init__(self, width, height, seed, config):
        self.width = width
        self.height = height
        self.seed = seed
        self.config = config
        self.time = 0
        self.drawables = {}
        self.store = {}

    @property
    def all_drawables(self):
        result = []
        for key in self.drawables:
            result.extend(self.drawables[key])
        return result

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    @property
    def corners(self):
        return Point(0, 0), Point(self.width, self.height)

    def is_inside(self, point: Point, offset=0):
        is_x_inside = offset <= point.x <= (self.width - offset)
        is_y_inside = offset <= point.y <= (self.height - offset)
        return is_x_inside and is_y_inside

    def get_closest_edge(self, drawable):
        left = Point(0, drawable.position.y)
        top = Point(drawable.position.x, 0)
        right = Point(self.width, drawable.position.y)
        bottom = Point(drawable.position.x, self.height)
        return drawable.position.find_closest((left, top, right, bottom))

    def __getitem__(self, key):
        return self.drawables[key]

    def __setitem__(self, key, value):
        self.drawables[key] = value
