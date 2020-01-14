from world import World


class WorldController(object):
    def __init__(self, canvas, canvas_length, world_data=None):
        self.canvas = canvas
        self.canvas_length = canvas_length
        self.ANIMAL_DIAMETER = 5
        if world_data is None:
            self.world = World(self.canvas_length)
        else:
            self.world = self.load_world(world_data)

    # TODO: Implement loading of world from JSON file
    def load_world(self, world_data):
        return

    # TODO: Implement saving of world as JSON file
    def save_world(self):
        pass

    def start_simulation(self):
        self.world.start_world()
        self.update_canvas()

    def update_canvas(self):
        self.draw_all_animals()

    def draw_all_animals(self):
        self.canvas.delete('all')
        for animal in self.world.all_animals:
            self.draw_animal(animal)
        self.canvas.update()

    def draw_animal(self, animal):
        circle_coordinates = animal.x, animal.y, animal.x + self.ANIMAL_DIAMETER, animal.y + self.ANIMAL_DIAMETER
        self.canvas.create_oval(circle_coordinates, fill=animal.DNA.color)

    def run_world(self):
        self.world.run()
        if self.world.is_running():
            self.update_canvas()


