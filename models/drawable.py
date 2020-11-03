import abc

from structs.color import Color
from structs.point import Point


class Drawable(abc.ABC):
    def __init__(self, position: Point, radius, color: Color):
        self.position = position
        self.last_position = position
        self.radius = radius
        self.color = color
        self.canvas_id = None
        self.can_remove = False

    def remove(self):
        self.can_remove = True

