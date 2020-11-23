from models.animal import Animal
from structs.point import Point
from models.drawable import Drawable


# abstract all_animals and all_food so that world doesn't know the concept of animals/food
class World:
    def __init__(self, width, height, seed):
        self.width = width
        self.height = height
        self.seed = seed
        self.time = 0
        self.all_animals = []
        self.all_food = []
        self.config = {}

    def add_animal(self, animal):
        self.all_animals.append(animal)

    @property
    def all_drawables(self):
        result = []
        result.extend(self.all_animals)
        result.extend(self.all_food)
        return result

    @property
    def all_active_animals(self):
        return [a for a in self.all_animals if not a.is_asleep]

    @property
    def center(self):
        return Point(self.width / 2, self.height / 2)

    @property
    def corners(self):
        return Point(0, 0), Point(self.width, self.height)

    @property
    def is_asleep(self):
        return all([a.is_asleep for a in self.all_animals]) or (len(self.all_food) == 0 and all([a.is_asleep for a in self.all_animals if a.foods_eaten > 0]))

    @property
    def is_dead(self):
        return not len(self.all_animals)

    def is_inside(self, point: Point, offset=0):
        is_x_inside = offset <= point.x <= (self.width - offset)
        is_y_inside = offset <= point.y <= (self.height - offset)
        return is_x_inside and is_y_inside

    def wipe(self):
        self.time = 0
        self.all_animals = []
        self.all_food = []

    def find_closest_food(self, animal: Animal):
        return animal.position.find_closest([food for food in self.all_food], get_position=lambda f: f.position)

    def get_closest_edge(self, drawable: Drawable):
        left = Point(drawable.radius, drawable.position.y)
        top = Point(drawable.position.x, drawable.radius)
        right = Point(self.width - drawable.radius, drawable.position.y)
        bottom = Point(drawable.position.x, self.height - drawable.radius)
        return drawable.position.find_closest((left, top, right, bottom))

    def remove_food(self, food):
        self.all_food.remove(food)
