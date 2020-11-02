from models.animal import Animal
from structs.color import Color
from structs.point import Point


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.time = 0
        self.all_animals = []
        self.all_food = []

    def create_animal(self, side=None, animal_class=Animal, color=Color(0, 0, 255)):
        new_animal = animal_class.random(*self.corners, side=side, color=color)
        self.all_animals.append(new_animal)

    @property
    def all_drawables(self):
        result = []
        result.extend(self.all_animals)
        result.extend(self.all_food)
        return result

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    @property
    def corners(self):
        return Point(0, 0), Point(self.width, self.height)

    @property
    def is_asleep(self):
        return False

    def is_inside(self, point: Point, offset=0):
        is_x_inside = offset <= point.x <= (self.width - offset)
        is_y_inside = offset <= point.y <= (self.height - offset)
        return is_x_inside and is_y_inside

    def wipe(self):
        self.time = 0
        self.all_animals = []
        self.all_food = []

    def filter_animals(self):
        self.all_animals = [a for a in self.all_animals if a.is_alive]

    def find_closest_food(self, animal: Animal):
        return animal.position.find_closest([food for food in self.all_food], get_position=lambda f: f.position)

    def get_closest_edge(self, animal: Animal):
        left = Point(animal.radius, animal.position.y)
        top = Point(animal.position.x, animal.radius)
        right = Point(self.width - animal.radius, animal.position.y)
        bottom = Point(animal.position.x, self.height - animal.radius)
        return animal.position.find_closest((left, top, right, bottom))
