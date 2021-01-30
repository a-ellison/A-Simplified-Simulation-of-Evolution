import math
from enum import Enum

from models.drawable import Drawable
from structs.color import Color

import helpers
from structs.point import Point

AnimalState = Enum("AnimalState", "ASLEEP ACTIVE")


class PrimerAnimal(Drawable):
    MIN_RADIUS = 3
    MAX_RADIUS = 8
    MIN_SPEED = 1
    MAX_SPEED = 10
    MIN_SIGHT_RANGE = MIN_RADIUS + 1
    MAX_SIGHT_RANGE = 25
    MIN_FOV = math.pi / 10
    MIN_TURN = math.pi / 10

    RADIUS_MUTATION = (MAX_RADIUS - MIN_RADIUS) / 20  # 5 percent
    SPEED_MUTATION = (MAX_SPEED - MIN_SPEED) / 20
    SIGHT_RANGE_MUTATION = (MAX_SIGHT_RANGE - MIN_SIGHT_RANGE) / 20

    MAX_ENERGY_FACTOR = 1  # set from behavior

    MIN_EDIBLE_SIZE = 200 / 10 ** 2
    MAX_EDIBLE_SIZE = 300 / 10 ** 2

    def __init__(self, position, radius, speed, sight_range):
        super().__init__(
            position, radius, PrimerAnimal.calculate_color(radius, speed, sight_range)
        )
        self.age = 0
        self.speed = speed
        self.max_energy = radius ** 3 * self.MAX_ENERGY_FACTOR
        self.energy = self.max_energy
        self.sight_range = sight_range
        self.objective = None
        self.last_objective = None
        self.foods_eaten = 0
        self.state = AnimalState.ACTIVE

    def move(self, min_coordinate, max_coordinate):
        self.last_position = self.position
        distance_to_target = self.position.distance_to(self.objective.position)
        distance = min(self.speed, distance_to_target)
        angle = self.position.angle_to(self.objective.position)
        min_coordinate = min_coordinate.move_by(self.radius)
        max_coordinate = max_coordinate.move_by(-self.radius)
        self.position = self.position.move_to(distance, angle).restrict_to(
            min_coordinate, max_coordinate
        )
        self.last_objective = self.objective

    @classmethod
    def calculate_step_cost(cls, r, d, s):
        return (r ** 4) * (d ** 2) * s

    def apply_step_cost(self):
        if self.has_moved:
            self.energy -= PrimerAnimal.calculate_step_cost(
                self.radius,
                self.position.distance_to(self.last_position),
                self.sight_range,
            )

    @property
    def has_moved(self):
        return self.last_objective is not None

    @property
    def field_of_view(self):
        return (
            math.pi
            - (math.pi / (PrimerAnimal.MAX_SIGHT_RANGE - PrimerAnimal.MIN_SIGHT_RANGE))
            * (self.sight_range - PrimerAnimal.MIN_SIGHT_RANGE)
            + PrimerAnimal.MIN_FOV
        )

    @property
    def max_turn(self):
        return (
            (math.pi / 2)
            * (self.speed - PrimerAnimal.MIN_SPEED) ** 2
            / (PrimerAnimal.MAX_SPEED - PrimerAnimal.MIN_SPEED) ** 2
        ) + PrimerAnimal.MIN_TURN

    @property
    def is_hungry(self):
        return self.foods_eaten < 2

    @property
    def is_alive(self):
        return self.energy > 0

    @property
    def is_asleep(self):
        return self.state == AnimalState.ASLEEP

    def can_see(self, position):
        return self.position.distance_to(position) <= self.sight_range

    def can_reach(self, position):
        return self.position.distance_to(position) - self.radius <= self.radius

    def add_objective(self, new_objective):
        if self.objective is None or new_objective.intensity > self.objective.intensity:
            self.objective = new_objective

    def eat(self):
        self.foods_eaten += 1

    def sleep(self):
        self.last_objective = None
        self.last_position = self.position
        self.state = AnimalState.ASLEEP

    def wake_up(self):
        self.energy = self.max_energy
        self.state = AnimalState.ACTIVE
        self.foods_eaten = 0

    def mutate(self):
        mutated_radius = helpers.mutate_value(
            PrimerAnimal.MIN_RADIUS,
            PrimerAnimal.MAX_RADIUS,
            self.radius,
            PrimerAnimal.RADIUS_MUTATION,
        )
        mutated_speed = helpers.mutate_value(
            PrimerAnimal.MIN_SPEED,
            PrimerAnimal.MAX_SPEED,
            self.speed,
            PrimerAnimal.SPEED_MUTATION,
        )
        mutated_sight_range = helpers.mutate_value(
            PrimerAnimal.MIN_SIGHT_RANGE,
            PrimerAnimal.MAX_SIGHT_RANGE,
            self.sight_range,
            PrimerAnimal.SIGHT_RANGE_MUTATION,
        )
        position = self.position.move_by(self.radius)
        return PrimerAnimal(
            position, mutated_radius, mutated_speed, mutated_sight_range
        )

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
        r = int(
            (255 / (PrimerAnimal.MAX_RADIUS - PrimerAnimal.MIN_RADIUS))
            * (radius - PrimerAnimal.MIN_RADIUS)
        )
        g = int(
            (255 / (PrimerAnimal.MAX_SPEED - PrimerAnimal.MIN_SPEED))
            * (speed - PrimerAnimal.MIN_SPEED)
        )
        b = int(
            (255 / (PrimerAnimal.MAX_SIGHT_RANGE - PrimerAnimal.MIN_SIGHT_RANGE))
            * (sight_range - PrimerAnimal.MIN_SIGHT_RANGE)
        )
        return Color(r, g, b)

    @classmethod
    def random(cls, min_coordinate, max_coordinate, side=None, **kwargs):
        radius = kwargs.get(
            "radius",
            helpers.random_decimal(PrimerAnimal.MIN_RADIUS, PrimerAnimal.MAX_RADIUS),
        )
        speed = kwargs.get(
            "speed",
            helpers.random_decimal(PrimerAnimal.MIN_SPEED, PrimerAnimal.MAX_SPEED),
        )
        sight_range = kwargs.get(
            "sight_range",
            helpers.random_decimal(
                PrimerAnimal.MIN_SIGHT_RANGE, PrimerAnimal.MAX_SIGHT_RANGE
            ),
        )
        min_coordinate = min_coordinate.move_by(radius)
        max_coordinate = max_coordinate.move_by(-radius)
        position = kwargs.get(
            "position", Point.random(min_coordinate, max_coordinate, side)
        )
        return PrimerAnimal(position, radius, speed, sight_range)
