from abc import ABC

from structs.color import Color
from structs.point import Point


class Drawable(ABC):
    def __init__(self, position: Point, radius, color: Color):
        self.position = position
        self.last_position = position
        self.last_drawn_position = position
        self.radius = radius
        self.color = color
        self.canvas_id = None
