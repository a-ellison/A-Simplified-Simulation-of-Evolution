from random import randint


class Point(object):
    used_points = []

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def random(cls, max_x, max_y):
        x = randint(0, max_x)
        y = randint(0, max_y)
        point = Point(x, y)
        while Point.find(point) != -1:
            x = randint(0, max_x)
            y = randint(0, max_y)
            point = Point(x, y)
        return point

    @classmethod
    def find(cls, target_point):
        left = 0
        right = len(Point.used_points) - 1
        parameter = 'x'
        while left <= right:
            mid = int(left + (right - left) / 2)
            mid_point = Point.used_points[mid]
            mid_value = mid_point.get_parameter(parameter)
            target_value = target_point.get_parameter(parameter)
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
    def insert(cls, point):
        if Point.find(point) != -1:
            return -1
        n = len(Point.used_points)
        if n == 0:
            Point.used_points.append(point)
            return 0
        i = 0
        while Point._compare(point, Point.used_points[i], 'x'):
            i += 1
            if i == n:
                Point.used_points.append(point)
                return 0
        while Point._compare(point, Point.used_points[i], 'y'):
            i += 1
            if i == n:
                Point.used_points.append(point)
                return 0
        Point.used_points.insert(i + 1, point)
        return 0

    @classmethod
    def _compare(cls, point_a, point_b, parameter):
        if parameter == 'all':
            return point_a == point_b
        else:
            return point_a.get_parameter(parameter) == point_b.get_parameter(parameter)


