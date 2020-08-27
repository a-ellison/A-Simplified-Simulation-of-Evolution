import logging


class World:
    def __init__(self, animal_class, width, height):
        self.animal_class = animal_class
        self.width = width
        self.height = height
        self.all_animals = []
        self.objects = {}
        logging.info('Initializing world')

    def create_animal(self):
        new_animal = self.animal_class.random(self.width, self.height)
        self.all_animals.append(new_animal)

    @property
    def all_objects(self):
        all = []
        all.extend(self.all_animals)
        for i in self.objects:
            all.extend(self.objects[i])
        return all
