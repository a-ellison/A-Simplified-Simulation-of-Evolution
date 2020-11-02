import abc

from structs.color import Color
from structs.point import Point


class Drawable(abc.ABC):
    def __init__(self, position: Point, radius, color: Color, shape='circle'):
        self.position = position
        self.last_position = position
        self.radius = radius
        self.color = color
        self.shape = shape
        self.canvas_id = None
