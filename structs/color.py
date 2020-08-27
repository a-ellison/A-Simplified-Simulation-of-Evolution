from random import randint


class Color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def random_hex_string(cls):
        return Color.random().to_hex()

    @classmethod
    def random(cls):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        color = Color(r, g, b)
        return color

    # uses Tkinter color formatting
    def to_hex(self):
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    @classmethod
    def from_hex(cls, hex_string):
        r = int(hex_string[1:3], 16)
        g = int(hex_string[3:5], 16)
        b = int(hex_string[5:7], 16)
        return Color(r, g, b)
