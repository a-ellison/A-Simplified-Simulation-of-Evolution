from random import randint


class Color(object):
    used_colors = []

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def random_hex_string(cls):
        return Color.random().to_hex_string()

    @classmethod
    def random(cls):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        color = Color(r, g, b)
        while Color.find(color) != -1:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            color = Color(r, g, b)
        return color

    # use binary search to find the target color in used_colors.
    # return index if color was found, otherwise -1
    @classmethod
    def find(cls, target_color):
        left = 0
        right = len(Color.used_colors) - 1
        parameter = 'r'
        while left <= right:
            mid = int(left + (right - left) / 2)
            mid_color = Color.used_colors[mid]
            mid_value = mid_color.get_parameter(parameter)
            target_value = target_color.get_parameter(parameter)

            if target_value == mid_value:
                if parameter == 'r':
                    parameter = 'g'
                elif parameter == 'g':
                    parameter = 'b'
                else:
                    return mid
            elif target_value > mid_value:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    @classmethod
    def insert(cls, color):
        if Color.find(color) != -1:
            return -1
        n = len(Color.used_colors)
        if n == 0:
            Color.used_colors.append(color)
            return 0
        i = 0
        while Color._compare(color, Color.used_colors[i], 'r'):
            i += 1
            if i == n:
                Color.used_colors.append(color)
                return 0
        while Color._compare(color, Color.used_colors[i], 'g'):
            i += 1
            if i == n:
                Color.used_colors.append(color)
                return 0
        while Color._compare(color, Color.used_colors[i], 'b'):
            if i == n:
                Color.used_colors.append(color)
                return 0
            i += 1
        Color.used_colors.insert(i + 1, color)
        return 0

    @classmethod
    def _compare(cls, color_a, color_b, parameter):
        if parameter == 'all':
            return color_a == color_b
        else:
            return color_a.get_parameter(parameter) == color_b.get_parameter(parameter)

    def get_parameter(self, parameter):
        if parameter == 'r':
            return self.r
        elif parameter == 'g':
            return self.g
        elif parameter == 'b':
            return self.b
        else:
            raise ValueError

    # uses Tkinter color formatting
    def to_hex_string(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    @classmethod
    def from_hex(cls, hex_string):
        r = int(hex_string[1:3], 16)
        g = int(hex_string[3:5], 16)
        b = int(hex_string[5:7], 16)
        return Color(r, g, b)
