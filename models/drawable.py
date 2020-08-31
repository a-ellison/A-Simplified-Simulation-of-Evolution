import abc


class Drawable(abc.ABC):
    def __init__(self, x, y, size, color, shape='circle'):
        self.x = x
        self.last_x = self.x
        self.y = y
        self.last_y = self.y
        self.size = size
        self.color = color
        self.shape = shape
        self.canvas_object = None
