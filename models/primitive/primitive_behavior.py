import random

from models.behavior import Behavior
from models.primitive import primitive_animal
import helper_functions


DECIMAL_PLACES = 2
MIN_EDIBLE_SIZE = 20 / 10 ** DECIMAL_PLACES
MAX_EDIBLE_SIZE = 50 / 10 ** DECIMAL_PLACES

START_POPULATION = 100

FOOD_LIST = 'food'


class PrimitiveBehavior(Behavior):
    ANIMAL = primitive_animal.PrimitiveAnimal

    @classmethod
    def initialize(cls, world):
        cls.generate_animals(world)
        cls.generate_food(world)

    @classmethod
    def generate_animals(cls, world):
        for i in range(int(START_POPULATION)):
            world.create_animal()

    @classmethod
    def generate_food(cls, world):
        world.objects[FOOD_LIST] = []
        for i in range(int(START_POPULATION * 0.75)):
            x = random.randint(int(world.width / 4), int(world.width * 3/4))
            y = random.randint(int(world.height) / 4, int(world.height * 3/4))
            size = helper_functions.random_decimal(MIN_EDIBLE_SIZE, MAX_EDIBLE_SIZE, DECIMAL_PLACES)
            food = Edible(x, y, size)
            world.objects[FOOD_LIST].append(food)

    @classmethod
    def apply(cls, world):
        for animal in world.all_animals:
            cls.orient(animal, world)
        for animal in world.all_animals:
            cls.move(animal, world)
        for animal in world.all_animals:
            cls.act(animal, world)

    @classmethod
    def orient(cls, animal, world):
        cls.add_food_objective(animal, world)
        cls.add_sleep_objective(animal, world)
        cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal, world):
        pass

    @classmethod
    def add_sleep_objective(cls, animal, world):
        pass

    @classmethod
    def add_wander_objective(cls, animal, world):
        PRIORITY = Objective.LOW

    @classmethod
    def move(cls, animal, world):
        pass

    @classmethod
    def act(cls, animal, world):
        pass


class Objective:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    def __init__(self, position, intensity, reason):
        self.position = position
        self.intensity = intensity
        self.reason = reason


class Edible:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = '#FFFFFF'
