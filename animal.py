class Animal(object):
    def __init__(self, start_x, start_y, DNA):
        self.x = start_x
        self.y = start_y
        self.DNA = DNA

    def move(self):
        self.x += self.DNA.speed
