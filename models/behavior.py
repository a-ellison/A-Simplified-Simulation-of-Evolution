import logging
import math
import random

import helpers
from helpers import Speed
from models.drawable import Drawable
from models.animal import Animal
from models import animal
from models.world import World
from structs.color import Color
from structs.point import Point


class Behavior:
    @classmethod
    def initialize(cls, world: World):
        cls.generate_animals(world)
        cls.generate_food(world)

    @classmethod
    def generate_animals(cls, world: World):
        species_count = max(0, min(world.config.get('start_population'), world.config.get('species')))
        species = cls.generate_species(world.corners, species_count)
        for i in range(world.config.get('start_population', 0)):
            if i % 4 == 0:
                side = Point.TOP
            elif i % 4 == 1:
                side = Point.RIGHT
            elif i % 4 == 2:
                side = Point.BOTTOM
            elif i % 4 == 3:
                side = Point.LEFT
            traits = species[i % species_count]
            new_animal = Animal.random(*world.corners, side=side, **traits)
            world.add_animal(new_animal)

    @classmethod
    def params(cls):
        return {
            'start_population': {
                'default': 40,
                'label': 'Start Population',
            },
            'food_count': {
                'default': 20,
                'label': 'Food Count',
            },
            'species': {
                'default': 3,
                'label': 'Species',
            },
        }

    @classmethod
    def generate_species(cls, corners, n):
        return [Animal.random(*corners).traits for _ in range(n)]

    @classmethod
    def generate_food(cls, world: World):
        for i in range(world.config.get('food_count', 0)):
            min_coordinate = Point(int(world.width / 6), int(world.height / 6))
            max_coordinate = Point(int(world.width * 5 / 6), int(world.height * 5 / 6))
            position = Point.random(min_coordinate, max_coordinate)
            radius = helpers.random_decimal(animal.MAX_EDIBLE_SIZE, animal.MAX_EDIBLE_SIZE)
            food = Edible(position, radius, Color(255, 255, 255))
            world.all_food.append(food)

    @classmethod
    def apply(cls, world: World, speed):
        if world.is_asleep:
            world.all_animals = [a for a in world.all_animals if a.is_asleep]
            cls.reset_day(world)
            logging.info('A day has passed...')
        else:
            import time
            delay = 0.01 if speed == Speed.SLOW else 0
            start = time.perf_counter()
            cls.orient(world)
            cls.move(world)
            cls.act(world)
            cls.reset_step(world)
            duration = time.perf_counter() - start
            if duration < delay:
                time.sleep(delay - duration)
        world.time += 1

    @classmethod
    def orient(cls, world: World):
        for animal in world.all_active_animals:
            # if intensity is equal, first one is chosen
            cls.add_food_objective(animal, world)
            cls.add_sleep_objective(animal, world)
            cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal: Animal, world: World):
        if animal.is_hungry:
            food = world.find_closest_food(animal)
            if food is not None and animal.can_see(food.position):
                if animal.foods_eaten == 0:
                    intensity = Objective.HIGH
                else:
                    intensity = Objective.MEDIUM
                animal.add_objective(Objective(food.position, intensity, 'food'))

    @classmethod
    def add_sleep_objective(cls, animal: Animal, world: World):
        if animal.foods_eaten > 0:
            home = world.get_closest_edge(animal)
            steps_to_home = home.distance_to(animal.position) / animal.speed
            last_step_cost = animal.step_cost
            cost_go_home = steps_to_home * last_step_cost
            quotient = animal.energy / cost_go_home
            if quotient < 2:
                intensity = Objective.HIGH
            elif quotient < 8:
                intensity = Objective.MEDIUM
            else:
                intensity = Objective.LOW
            animal.add_objective(Objective(home, intensity, 'sleep'))

    @classmethod
    def add_wander_objective(cls, animal: Animal, world: World):
        if not animal.has_moved:
            new_position = world.center
        else:
            angle = animal.last_position.angle_to(animal.last_objective.position)
            offset = math.radians(random.randint(-20, 20))
            angle += offset
            new_position = animal.position.move_to(animal.speed, angle)
            if not world.is_inside(new_position, offset=animal.radius):
                new_position = world.center
        animal.add_objective(Objective(new_position, Objective.MEDIUM, 'wandering'))

    @classmethod
    def move(cls, world: World):
        for animal in world.all_active_animals:
            animal.move(*world.corners)

    @classmethod
    def act(cls, world: World):
        cls.try_eat(world)
        cls.try_sleep(world)

    @classmethod
    def try_eat(cls, world: World):
        for animal in world.all_active_animals:
            food = world.find_closest_food(animal)
            if animal.is_hungry and food is not None and animal.can_reach(food.position):
                animal.eat(food)
                world.remove_food(food)

    @classmethod
    def try_sleep(cls, world: World):
        for animal in world.all_active_animals:
            if animal.foods_eaten > 0:
                home = world.get_closest_edge(animal)
                distance_to_home = animal.position.distance_to(home)
                if home is not None and distance_to_home < animal.radius:
                    animal.sleep()

    @classmethod
    def reset_step(cls, world: World):
        for animal in world.all_animals:
            animal.age += 1
            animal.apply_step_cost()
        world.all_animals = [a for a in world.all_animals if a.is_alive]

    @classmethod
    def reset_day(cls, world: World):
        world.all_animals = [a for a in world.all_animals if a.is_asleep]
        cls.generate_food(world)
        for animal in world.all_animals:
            if not animal.is_hungry:
                child = animal.mutate()
                world.add_animal(child)
            animal.wake_up()


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
