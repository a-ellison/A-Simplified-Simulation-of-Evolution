from models.drawable import Drawable
from structs.color import Color

import helper_functions
from structs.point import Point

MIN_RADIUS = 4
MAX_RADIUS = 6
RADIUS_MUTATION = 0.5
MIN_SPEED = 2
MAX_SPEED = 4
SPEED_MUTATION = 0.5
MIN_SIGHT_RANGE = 4
MAX_SIGHT_RANGE = 20
SIGHT_RANGE_MUTATION = 2
MOVEMENT_COST_FACTOR = 0.22
MAX_ENERGY_FACTOR = 1000

MIN_EDIBLE_SIZE = 200 / 10 ** 2
MAX_EDIBLE_SIZE = 300 / 10 ** 2


class Animal(Drawable):
    ASLEEP = 0
    ACTIVE = 1

    def __init__(self, position: Point, radius, speed, sight_range):
        super().__init__(position, radius, Animal.calculate_color(radius, speed, sight_range))
        self.age = 0
        self.speed = speed
        self.max_energy = (radius ** 3) * MAX_ENERGY_FACTOR
        self.energy = self.max_energy
        self.sight_range = sight_range
        self.objective = None
        self.last_objective = None
        self.foods_eaten = 0
        self.state = self.ACTIVE

    def move(self, min_coordinate, max_coordinate):
        self.last_position = self.position
        distance_to_target = self.position.distance_to(self.objective.position)
        distance = min(self.speed, distance_to_target)
        angle = self.position.angle_to(self.objective.position)
        min_coordinate = min_coordinate.move_by(self.radius)
        max_coordinate = max_coordinate.move_by(-self.radius)
        self.position = self.position.move_to(distance, angle).restrict_to(min_coordinate, max_coordinate)
        self.last_objective = self.objective
        self.objective = None

    @property
    def step_cost(self):
        distance_moved = self.position.distance_to(self.last_position)
        movement_cost = (self.radius ** 3) * (distance_moved ** 2)
        return movement_cost * MOVEMENT_COST_FACTOR + self.sight_range

    def apply_step_cost(self):
        if self.has_moved:
            self.energy -= self.step_cost

    @property
    def has_moved(self):
        return self.last_objective is not None

    @property
    def is_hungry(self):
        return self.foods_eaten < 2

    @property
    def is_alive(self):
        return self.energy > 0

    @property
    def is_asleep(self):
        return self.state == self.ASLEEP

    def can_see(self, position: Point):
        return self.position.distance_to(position) <= self.sight_range

    def can_reach(self, position: Point):
        return self.position.distance_to(position) - self.radius <= self.radius

    def add_objective(self, new_objective):
        if self.objective is None or new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    def eat(self, edible):
        self.foods_eaten += 1
        # self.energy += self.max_energy * (edible.radius ** 3 / self.radius ** 3)

    def sleep(self):
        self.last_objective = None
        self.last_position = self.position
        self.state = self.ASLEEP

    def wake_up(self):
        self.energy = self.max_energy
        self.state = self.ACTIVE
        self.foods_eaten = 0

    def mutate(self):
        mutated_radius = helper_functions.mutate_value(MIN_RADIUS, MAX_RADIUS, self.radius, RADIUS_MUTATION)
        mutated_speed = helper_functions.mutate_value(MIN_SPEED, MAX_SPEED, self.speed, SPEED_MUTATION)
        mutated_sight_range = helper_functions.mutate_value(MIN_SIGHT_RANGE, MAX_SIGHT_RANGE, self.sight_range,
                                                            SIGHT_RANGE_MUTATION)
        position = self.position.move_by(self.radius)
        color = Animal.calculate_color(mutated_radius, mutated_speed, mutated_sight_range)
        return Animal(position, mutated_radius, mutated_speed, mutated_sight_range)

    @property
    def traits(self):
        return dict(
            radius=self.radius,
            color=self.color,
            speed=self.speed,
            sight_range=self.sight_range,
        )

    @classmethod
    def calculate_color(cls, radius, speed, sight_range):
        r = int((255 / (MAX_RADIUS - MIN_RADIUS)) * (radius - MIN_RADIUS))
        g = int((255 / (MAX_SPEED - MIN_SPEED)) * (speed - MIN_SPEED))
        b = int((255 / (MAX_SIGHT_RANGE - MIN_SIGHT_RANGE)) * (sight_range - MIN_SIGHT_RANGE))
        return Color(r, g, b)

    @classmethod
    def random(cls, min_coordinate: Point, max_coordinate: Point, side=None, **kwargs):
        radius = kwargs.get('radius')
        if radius is None:
            radius = helper_functions.random_decimal(MIN_RADIUS, MAX_RADIUS)
        speed = kwargs.get('speed')
        if speed is None:
            speed = helper_functions.random_decimal(MIN_SPEED, MAX_SPEED)
        sight_range = kwargs.get('sight_range')
        if sight_range is None:
            sight_range = helper_functions.random_decimal(MIN_SIGHT_RANGE, MAX_SIGHT_RANGE)
        color = kwargs.get('color')
        position = kwargs.get('position')
        if position is None:
            min_coordinate = min_coordinate.move_by(radius)
            max_coordinate = max_coordinate.move_by(-radius)
            position = Point.random(min_coordinate, max_coordinate, side)
        return Animal(position, radius, speed, sight_range)
