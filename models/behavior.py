import logging
import math
import random

from models.drawable import Drawable
from models.animal import Animal
from models.world import World
from structs.color import Color
import helper_functions
from structs.point import Point

DECIMAL_PLACES = 2
MIN_EDIBLE_SIZE = 400 / 10 ** DECIMAL_PLACES
MAX_EDIBLE_SIZE = 600 / 10 ** DECIMAL_PLACES

FOOD_LIST = 'food'


class Behavior:
    @classmethod
    def initialize(cls, world: World, start_population, food_count):
        cls.generate_animals(world, start_population)
        cls.generate_food(world, food_count)

    @classmethod
    def generate_animals(cls, world: World, start_population):
        for i in range(start_population):
            if i % 4 == 0:
                world.create_animal(side='top')
            elif i % 4 == 1:
                world.create_animal(side='right')
            elif i % 4 == 2:
                world.create_animal(side='bottom')
            elif i % 4 == 3:
                world.create_animal(side='left')

    @classmethod
    def generate_food(cls, world: World, food_count):
        for i in range(food_count):
            top_left = Point(int(world.width / 6), int(world.width / 6))
            bottom_right = Point(int(world.height * 5 / 6), int(world.height * 5 / 6))
            position = Point.random(top_left, bottom_right)
            radius = helper_functions.random_decimal(MIN_EDIBLE_SIZE, MAX_EDIBLE_SIZE, DECIMAL_PLACES)
            food = Edible(position, radius, Color(i * 120 % 255, 0, 120))
            world.all_food.append(food)

    @classmethod
    def apply(cls, world: World):
        if world.is_asleep:
            # cls.reset_day()
            logging.info('A day has passed...')
            return
        else:
            cls.orient(world)
            cls.move(world)
            cls.act(world)
            cls.reset_step(world)
        world.time += 1

    @classmethod
    def orient(cls, world: World):
        for animal in world.all_animals:
            # if intensity is equal, first one is chosen
            cls.add_food_objective(animal, world)
            cls.add_sleep_objective(animal, world)
            cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal: Animal, world: World):
        food = world.find_closest_food(animal)
        if food is not None and animal.can_see(food.position):
            animal.add_objective(Objective(food.position, Objective.HIGH, 'food'))

    @classmethod
    def add_sleep_objective(cls, animal: Animal, world: World):
        # if animal.foods_eaten > 0:
        if False:
            home = world.get_closest_edge(animal)
            steps_to_home = home.distance_to(animal.position) / animal.speed
            last_step_cost = animal.step_cost
            quotient = steps_to_home / last_step_cost
            # determine good ranges for intensities

    @classmethod
    def add_wander_objective(cls, animal: Animal, world: World):
        if animal.age == 0:
            new_position = world.center
        else:
            angle = animal.last_position.angle_to(animal.last_objective.position)
            offset = math.radians(random.randint(-10, 10))
            angle += offset
            new_position = animal.position.move_to(animal.speed, angle)
            if not world.is_inside(new_position, offset=animal.radius):
                new_position = world.center
        animal.add_objective(Objective(new_position, Objective.LOW, 'wandering'))

    @classmethod
    def move(cls, world: World):
        for animal in world.all_animals:
            animal.move(*world.corners)

    @classmethod
    def act(cls, world: World):
        for animal in world.all_animals:
            food = world.find_closest_food(animal)
            if food is not None and animal.can_reach(food.position):
                animal.eat(food)
                world.all_food.remove(food)

    @classmethod
    def reset_step(cls, world: World):
        for animal in world.all_animals:
            animal.age += 1
            # animal.apply_step_cost()
        world.filter_animals()


class Objective:
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __init__(self, position: Point, intensity, reason):
        self.position = position
        self.intensity = intensity
        self.reason = reason


class Edible(Drawable):
    def __init__(self, position: Point, radius, color=Color(255, 255, 255)):
        super().__init__(position, radius, color)
