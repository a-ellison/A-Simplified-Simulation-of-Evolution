from abc import ABC

import helpers
from structs.color import Color
from structs.point import Point


# TODO: remove last_position, only used in primer animal
class Drawable(ABC):
    def __init__(self, position: Point, radius, color: Color):
        self.position = position
        self.last_position = position
        self.last_drawn_position = position
        self.radius = radius
        self.color = color
        self.canvas_id = None
