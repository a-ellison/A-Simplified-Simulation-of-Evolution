import time
import math
import random

from helpers import Speed
from models.behavior_base import BehaviorBase
from models.drawable import Drawable
from models.primer.animal import PrimerAnimal
from models.primer.data import PrimerData
from structs.color import Color
from structs.point import Point

ANIMALS = "ANIMALS"
FOOD = "FOOD"


class PrimerBehavior(BehaviorBase):
    @classmethod
    def initialize(cls, world):
        cls.set_constants(world)
        world.drawables[ANIMALS] = []
        world.drawables[FOOD] = []
        cls.generate_animals(world)
        cls.generate_food(world)

    @classmethod
    def set_constants(cls, world):
        width = world.width
        r = PrimerAnimal.MIN_RADIUS
        v = PrimerAnimal.MAX_SPEED
        s = PrimerAnimal.MAX_SIGHT_RANGE
        steps = width / v
        step_cost = PrimerAnimal.calculate_step_cost(r, v, s)
        factor = steps * step_cost / (r ** 3)
        PrimerAnimal.MAX_ENERGY_FACTOR = factor / 2

    @classmethod
    def get_data_collector(cls, world, **kwargs):
        return PrimerData(world, **kwargs)

    @classmethod
    def generate_animals(cls, world):
        species_count = max(
            0, min(world.config["start_population"], world.config["species"])
        )
        species = cls.generate_species(world.corners, species_count)
        for i in range(world.config["start_population"]):
            if i % 4 == 0:
                side = Point.TOP
            elif i % 4 == 1:
                side = Point.RIGHT
            elif i % 4 == 2:
                side = Point.BOTTOM
            elif i % 4 == 3:
                side = Point.LEFT
            traits = species[i % species_count]
            new_animal = PrimerAnimal.random(*world.corners, side=side, **traits)
            cls.add_animal(world, new_animal)

    @classmethod
    def add_animal(cls, world, animal):
        world.drawables[ANIMALS].append(animal)

    @classmethod
    def add_food(cls, world, food):
        world.drawables[FOOD].append(food)

    @classmethod
    def all_active_animals(cls, world):
        return [a for a in world.drawables[ANIMALS] if not a.is_asleep]

    @classmethod
    def is_asleep(cls, world):
        all_animals = cls.all_animals(world)
        return all([a.is_asleep for a in all_animals]) or (
            len(cls.all_food(world)) == 0
            and all([a.is_asleep for a in all_animals if a.foods_eaten > 0])
        )

    @classmethod
    def is_dead(cls, world):
        return not len(cls.all_animals(world))

    @classmethod
    def find_closest_food(cls, world, animal: PrimerAnimal):
        all_food = cls.all_food(world)
        return animal.position.find_closest(
            [food for food in all_food], get_position=lambda f: f.position
        )

    @classmethod
    def all_animals(cls, world):
        return world.drawables[ANIMALS]

    @classmethod
    def all_food(cls, world):
        return world.drawables[FOOD]

    @classmethod
    def remove_food(cls, world, food):
        world.drawables[FOOD].remove(food)

    @classmethod
    def get_config(cls):
        return {
            "start_population": {
                "default": 40,
                "label": "Start Population",
            },
            "food_count": {
                "default": 40,
                "label": "Food Count",
            },
            "species": {
                "default": 3,
                "label": "Species",
            },
        }

    @classmethod
    def generate_species(cls, corners, n):
        return [PrimerAnimal.random(*corners).traits for _ in range(n)]

    @classmethod
    def generate_food(cls, world):
        for i in range(world.config.get("food_count", 0)):
            min_coordinate = Point(int(world.width / 6), int(world.height / 6))
            max_coordinate = Point(int(world.width * 5 / 6), int(world.height * 5 / 6))
            position = Point.random(min_coordinate, max_coordinate)
            food = Edible(position)
            cls.add_food(world, food)

    @classmethod
    def apply(cls, world, speed):
        start = time.perf_counter()
        if cls.is_asleep(world):
            world.drawables[ANIMALS] = [
                a for a in cls.all_animals(world) if a.is_asleep
            ]
            cls.reset_day(world)
        else:
            cls.orient(world)
            cls.move(world)
            cls.act(world)
            cls.reset_step(world)
        duration = time.perf_counter() - start
        if speed == Speed.SLOW:
            delay = 0.05
        elif speed == Speed.NORMAL:
            delay = 0.01
        elif speed == Speed.FAST:
            delay = 0
        if duration < delay:
            time.sleep(delay - duration)
        return duration

    @classmethod
    def orient(cls, world):
        for animal in cls.all_active_animals(world):
            # if intensity is equal, first one is chosen
            cls.add_food_objective(animal, world)
            cls.add_sleep_objective(animal, world)
            cls.add_wander_objective(animal, world)

    @classmethod
    def add_food_objective(cls, animal: PrimerAnimal, world):
        if animal.is_hungry:
            food = cls.find_closest_food(world, animal)
            if food is not None and animal.can_see(food.position):
                if animal.foods_eaten == 0:
                    intensity = Objective.HIGH
                else:
                    intensity = Objective.MEDIUM
                animal.add_objective(
                    Objective(food.position, intensity, Objective.FOOD)
                )

    @classmethod
    def add_sleep_objective(cls, animal: PrimerAnimal, world):
        if animal.foods_eaten > 0:
            home = cls.find_home(animal, world)
            steps_to_home = home.distance_to(animal.position) / animal.speed
            step_cost = animal.calculate_step_cost(
                animal.radius, animal.speed, animal.sight_range
            )
            cost_go_home = steps_to_home * step_cost
            try:
                quotient = animal.energy / cost_go_home
            except ZeroDivisionError:
                quotient = float("inf")
            if (
                quotient < 1.5
                or animal.foods_eaten == 2
                or animal.last_objective.reason == Objective.SLEEP
            ):
                intensity = Objective.HIGH
            else:
                intensity = Objective.LOW
            animal.add_objective(Objective(home, intensity, Objective.SLEEP))

    @classmethod
    def find_home(cls, animal, world):
        min_coordinate, max_coordinate = world.corners
        edge = world.get_closest_edge(animal)
        if edge.x == min_coordinate.x:
            home = edge.move_by(animal.radius, 0)
        elif edge.y == min_coordinate.y:
            home = edge.move_by(0, animal.radius)
        elif edge.x == max_coordinate.x:
            home = edge.move_by(-animal.radius, 0)
        elif edge.y == max_coordinate.y:
            home = edge.move_by(0, -animal.radius)
        return home

    @classmethod
    def add_wander_objective(cls, animal: PrimerAnimal, world):
        if not animal.has_moved:
            new_position = world.center
        else:
            angle = animal.last_position.angle_to(animal.last_objective.position)
            offset = math.radians(random.randint(-20, 20))
            angle += offset
            new_position = animal.position.move_to(animal.speed, angle)
            if not world.is_inside(new_position, offset=animal.radius):
                new_position = world.center
        animal.add_objective(
            Objective(new_position, Objective.MEDIUM, Objective.WANDER)
        )

    @classmethod
    def move(cls, world):
        for animal in cls.all_active_animals(world):
            animal.move(*world.corners)

    @classmethod
    def act(cls, world):
        cls.try_eat(world)
        cls.try_sleep(world)

    @classmethod
    def try_eat(cls, world):
        for animal in cls.all_active_animals(world):
            food = cls.find_closest_food(world, animal)
            if (
                animal.is_hungry
                and food is not None
                and animal.can_reach(food.position)
            ):
                animal.eat()
                cls.remove_food(world, food)

    @classmethod
    def try_sleep(cls, world):
        for animal in cls.all_active_animals(world):
            wants_sleep = (
                animal.objective is not None
                and animal.objective.reason == Objective.SLEEP
            )
            if animal.foods_eaten > 0 and wants_sleep:
                home = cls.find_home(animal, world)
                distance_to_home = animal.position.distance_to(home)
                if distance_to_home == 0:
                    animal.sleep()

    @classmethod
    def reset_step(cls, world):
        for animal in cls.all_animals(world):
            animal.objective = None
            animal.apply_step_cost()
        alive = []
        for a in cls.all_animals(world):
            if a.is_alive:
                alive.append(a)
            else:
                del a
        world.drawables[ANIMALS] = alive

    @classmethod
    def reset_day(cls, world):
        world.drawables[ANIMALS] = [a for a in cls.all_animals(world) if a.is_asleep]
        cls.generate_food(world)
        for animal in cls.all_animals(world):
            if not animal.is_hungry:
                child = animal.mutate()
                cls.add_animal(world, child)
            animal.wake_up()
            animal.age += 1


class Objective:
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    WANDER = "wander"
    SLEEP = "sleep"
    FOOD = "food"

    def __init__(self, position, intensity, reason):
        self.position = position
        self.intensity = intensity
        self.reason = reason


class Edible(Drawable):
    EDIBLE_RADIUS = 2.5

    def __init__(self, position):
        super().__init__(position, self.EDIBLE_RADIUS, Color(255, 255, 255))
