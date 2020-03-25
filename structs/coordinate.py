from random import randint


class Coordinate(object):
    used_coordinates = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def scaled_to(self, scale_factor):
        return Coordinate(self.x * 1 / scale_factor, self.y * 1 / scale_factor)

    @classmethod
    def random(cls, max_x, max_y):
        x = randint(0, max_x)
        y = randint(0, max_y)
        coordinate = Coordinate(x, y)
        while Coordinate.find(coordinate) != -1:
            x = randint(0, max_x)
            y = randint(0, max_y)
            coordinate = Coordinate(x, y)
        return coordinate

    @classmethod
    def find(cls, target_coordinate):
        left = 0
        right = len(Coordinate.used_coordinates) - 1
        parameter = 'x'
        while left <= right:
            mid = int(left + (right - left) / 2)
            mid_coordinate = Coordinate.used_coordinates[mid]
            mid_value = mid_coordinate.get_parameter(parameter)
            target_value = target_coordinate.get_parameter(parameter)
            if target_value == mid_value:
                if parameter == 'x':
                    parameter = 'y'
                else:
                    return mid
            elif target_value > mid_value:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def get_parameter(self, parameter):
        if parameter == 'x':
            return self.x
        elif parameter == 'y':
            return self.y
        else:
            raise ValueError

    @classmethod
    def insert(cls, coordinate):
        if Coordinate.find(coordinate) != -1:
            return -1
        n = len(Coordinate.used_coordinates)
        if n == 0:
            Coordinate.used_coordinates.append(coordinate)
            return 0
        i = 0
        while Coordinate._compare(coordinate, Coordinate.used_coordinates[i], 'x'):
            i += 1
            if i == n:
                Coordinate.used_coordinates.append(coordinate)
                return 0
        while Coordinate._compare(coordinate, Coordinate.used_coordinates[i], 'y'):
            i += 1
            if i == n:
                Coordinate.used_coordinates.append(coordinate)
                return 0
        Coordinate.used_coordinates.insert(i + 1, coordinate)
        return 0

    @classmethod
    def _compare(cls, coordinate_a, coordinate_b, parameter):
        if parameter == 'all':
            return coordinate_a == coordinate_b
        else:
            return coordinate_a.get_parameter(parameter) == coordinate_b.get_parameter(parameter)


