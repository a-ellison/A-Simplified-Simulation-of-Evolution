import logging
import math
import random

from models import drawable
from models.behavior import Behavior
from models.primitive import primitive_animal
from structs.color import Color
import helper_functions

DECIMAL_PLACES = 2
MIN_EDIBLE_SIZE = 300 / 10 ** DECIMAL_PLACES
MAX_EDIBLE_SIZE = 400 / 10 ** DECIMAL_PLACES

START_POPULATION = 1

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
            cls.create_animal(world)

    @classmethod
    def create_animal(cls, world):
        new_animal = primitive_animal.PrimitiveAnimal.random(world.width, world.height, color=Color(0, 0, 255))
        world.all_animals.append(new_animal)

    @classmethod
    def generate_food(cls, world):
        world.objects[FOOD_LIST] = []
        for i in range(int(START_POPULATION * 2)):
            x = random.randint(int(world.width / 4), int(world.width * 3 / 4))
            y = random.randint(int(world.height / 4), int(world.height * 3 / 4))
            size = helper_functions.random_decimal(MIN_EDIBLE_SIZE, MAX_EDIBLE_SIZE, DECIMAL_PLACES)
            food = Edible(x, y, size, Color(i * 120, 0, 120))
            world.objects[FOOD_LIST].append(food)

    @classmethod
    def apply(cls, world):
        for animal in world.all_animals:
            cls.orient(animal, world)
        for animal in world.all_animals:
            animal.move(world.width, world.height)
        # for animal in world.all_animals:
        #     cls.act(animal, world)

    @classmethod
    def orient(cls, animal, world):
        cls.add_food_objective(animal, world)
        cls.add_sleep_objective(animal, world)
        cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal, world):
        food = cls.find_closest_food(animal, world)
        logging.info(f'Color of closest food: {food.color.to_hex()}')
        # if animal.can_see(food):
        #     animal.add_objective(Objective(food.x, food.y, Objective.HIGH, 'food'))

    @classmethod
    def find_closest_food(cls, animal, world):
        min_distance = float('inf')
        for food in world.objects[FOOD_LIST]:
            distance = helper_functions.distance_to(animal.x, animal.y, food.x, food.y)
            if distance < min_distance:
                closest_food = food
        return closest_food

    @classmethod
    def add_sleep_objective(cls, animal, world):
        pass

    @classmethod
    def add_wander_objective(cls, animal, world):
        if not animal.has_moved:
            x, y = world.center
        else:
            offset = math.radians(random.randint(-10, 10))
            direction = helper_functions.angle_to(animal.last_x, animal.last_y, animal.last_objective.x, animal.last_objective.y)
            direction += offset
            distance = animal.speed
            x, y = helper_functions.move_to(animal.x, animal.y, direction, distance)
            if not world.is_inside(x, y):
                x, y = world.center
        animal.add_objective(Objective(x, y, Objective.LOW, 'wandering'))

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

    def __init__(self, x, y, intensity, reason):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.reason = reason


class Edible(drawable.Drawable):
    def __init__(self, x, y, size, color=Color(255, 255, 255)):
        super().__init__(x, y, size, color)
