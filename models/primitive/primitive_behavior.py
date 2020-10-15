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

FOOD_LIST = 'food'


class PrimitiveBehavior(Behavior):
    ANIMAL = primitive_animal.PrimitiveAnimal

    @classmethod
    def initialize(cls, world, start_population, food_count):
        cls.generate_animals(world, start_population)
        cls.generate_food(world, food_count)

    @classmethod
    def generate_animals(cls, world, start_population):
        for i in range(4):
            for k in range(int(start_population / 4)):
                if i == 0:
                    cls.create_animal(world, side='top')
                elif i == 1:
                    cls.create_animal(world, side='right')
                elif i == 2:
                    cls.create_animal(world, side='bottom')
                elif i == 3:
                    cls.create_animal(world, side='left')

    @classmethod
    def create_animal(cls, world, side=None, color=Color(0, 0, 255)):
        new_animal = primitive_animal.PrimitiveAnimal.random(world.width, world.height, side=side, color=color)
        world.all_animals.append(new_animal)

    @classmethod
    def generate_food(cls, world, food_count):
        world.objects[FOOD_LIST] = []
        for i in range(food_count):
            x = random.randint(int(world.width / 6), int(world.width * 5 / 6))
            y = random.randint(int(world.height / 6), int(world.height * 5 / 6))
            size = helper_functions.random_decimal(MIN_EDIBLE_SIZE, MAX_EDIBLE_SIZE, DECIMAL_PLACES)
            food = Edible(x, y, size, Color(i * 120 % 255, 0, 120))
            world.objects[FOOD_LIST].append(food)

    @classmethod
    def apply(cls, world):
        for animal in world.all_animals:
            cls.orient(animal, world)
        for animal in world.all_animals:
            animal.move(world.width, world.height)
        for animal in world.all_animals:
            cls.act(animal, world)
        for animal in world.all_animals:
            cls.reset(animal, world)

    @classmethod
    def orient(cls, animal, world):
        cls.add_food_objective(animal, world)
        cls.add_sleep_objective(animal, world)
        cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal, world):
        food = cls.find_closest_food(animal, world)
        if food is not None and animal.can_see(food):
            animal.add_objective(Objective(food.x, food.y, Objective.HIGH, 'food'))

    @classmethod
    def find_closest_food(cls, animal, world):
        min_distance = float('inf')
        closest_food = None
        for food in world.objects[FOOD_LIST]:
            distance = helper_functions.distance_to(animal.x, animal.y, food.x, food.y)
            if distance < min_distance:
                min_distance = distance
                closest_food = food
        return closest_food

    @classmethod
    def add_sleep_objective(cls, animal, world):
        pass

    @classmethod
    def add_wander_objective(cls, animal, world):
        if animal.age == 0:
            x, y = world.center
        else:
            offset = math.radians(random.randint(-10, 10))
            direction = helper_functions.angle_to(animal.last_x, animal.last_y, animal.last_objective.x,
                                                  animal.last_objective.y)
            direction += offset
            distance = animal.speed
            x, y = helper_functions.move_to(animal.x, animal.y, direction, distance)
            if not world.is_inside(x, y):
                x, y = world.center
        animal.add_objective(Objective(x, y, Objective.LOW, 'wandering'))

    @classmethod
    def act(cls, animal, world):
        food = cls.find_closest_food(animal, world)
        if food is not None and animal.can_reach(food):
            animal.consume(food)
            logging.info(f'Found food after {animal.age} steps')
            world.objects[FOOD_LIST].remove(food)

    # TODO: determine energy cost for per step
    @classmethod
    def reset(cls, animal, world):
        animal.age += 1


class Objective:
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __init__(self, x, y, intensity, reason):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.reason = reason


class Edible(drawable.Drawable):
    def __init__(self, x, y, size, color=Color(255, 255, 255)):
        super().__init__(x, y, size, color)
