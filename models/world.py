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
