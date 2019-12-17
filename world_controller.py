from world import World


class World_Controller(object):
    def __init__(self, canvas, canvas_length, world=None):
        self.cv = canvas
        self.canvas_length = canvas_length
        self.animal_diameter = 5
        if world is None:
            self.world = World(self.canvas_length)
        else:
            # load world
            pass

    def draw_animals(self):
        self.cv.delete('all')
        for animal in self.world.all_animals:
            # coordinates for circle
            coords = animal.x, animal.y, animal.x + self.animal_diameter, animal.y + self.animal_diameter
            self.cv.create_oval(coords, fill=animal.color)
        self.cv.update()

    def start_simulation(self):
        self.world.start_world()
        self.draw_animals()

