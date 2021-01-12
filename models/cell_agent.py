from models.drawable import Drawable
from structs.point import Point


class CellAgent(Drawable):
    CELL_SIZE = 5
    STEP_COST = 1

    def __init__(self, cell_position, color):
        self.cell_position = cell_position
        super().__init__(self.to_actual_position(self.cell_position), self.CELL_SIZE / 2, color)
        self.age = 0

    def update_position(self):
        self.position = self.to_actual_position(self.cell_position)

    @classmethod
    def to_actual_position(cls, cell_position):
        x = cell_position.x * cls.CELL_SIZE + cls.CELL_SIZE / 2
        y = cell_position.y * cls.CELL_SIZE + cls.CELL_SIZE / 2
        return Point(x, y)

