from world import World


class WorldController(object):
    def __init__(self, canvas, canvas_width, canvas_height, scale_factor, world_data=None):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.scale_factor = scale_factor
        if world_data is None:
            self.world = World(self.canvas_width*self.scale_factor, self.canvas_height*self.scale_factor)
        else:
            self.world = self.load_world(world_data)

    # TODO: Implement loading world from JSON file
    def load_world(self, world_data):
        raise NotImplementedError

    # TODO: Implement saving world to JSON file
    def save_world(self):
        raise NotImplementedError

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
        coordinate = animal.get_coordinate().scaled_to(self.scale_factor)
        scaled_size = animal.get_size() / self.scale_factor
        self.canvas.create_circle(coordinate.x, coordinate.y, scaled_size, fill=animal.get_color())

    def run_world(self):
        self.run_tests()
        self.world.run()
        if self.world.is_running():
            self.update_canvas()

    def run_tests(self):
        pass


