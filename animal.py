def create_animal(animal1, animal2):
    pass


class Animal(object):
    def __init__(self, speed, color, DNA=None):
        self.DNA = DNA
        self.color = color
        self.speed = speed
        if DNA is None:
            pass

