class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.all_animals = []
        self.objects = {}

    @property
    def all_drawables(self):
        all = []
        all.extend(self.all_animals)
        for i in self.objects:
            all.extend(self.objects[i])
        return all

    @property
    def center(self):
        return self.width / 2, self.height / 2

    def is_inside(self, x, y):
        return 0 < x < self.width and 0 < y < self.height

    def wipe(self):
        self.all_animals = []
        self.objects = {}
