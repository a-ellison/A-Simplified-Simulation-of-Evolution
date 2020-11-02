import concurrent.futures
import logging

from models.simulation import Simulation

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class SimulationController(object):
    PAUSE = 0
    PLAY = 1
    RUNNING = 2

    def __init__(self, canvas, start_population, food_count):
        self.canvas = canvas
        self.state = SimulationController.PAUSE
        self.speed = 1
        self.start_population = start_population
        self.food_count = food_count
        self.simulation = Simulation(self.canvas.master.canvas_width, self.canvas.master.canvas_height, start_population, food_count)
        self.initialize_canvas()

    def initialize_canvas(self):
        for drawable in self.simulation.all_drawables:
            canvas_id = self.canvas.create_circle(drawable.position.x, drawable.position.y, drawable.radius, fill=drawable.color.to_hex())
            drawable.canvas_id = canvas_id

    def update_canvas(self):
        all_canvas_ids = list(self.canvas.find_all())
        for drawable in self.simulation.all_drawables:
            dx = drawable.position.x - drawable.last_position.x
            dy = drawable.position.y - drawable.last_position.y
            self.canvas.move(drawable.canvas_id, dx, dy)
            all_canvas_ids.remove(drawable.canvas_id)
        for unused in all_canvas_ids:
            self.canvas.delete(unused)
        self.canvas.update()

    def play(self):
        if self.state != SimulationController.RUNNING:
            logging.info('Playing simulation')
            self.state = SimulationController.RUNNING

            def callback(this_future):
                if not this_future._result:
                    raise BaseException('An error has ocurred: ' + str(this_future._exception))
                self.update_canvas()
                if self.state != SimulationController.PAUSE:
                    self.state = SimulationController.PLAY
                    self.play()

            future = thread_pool.submit(self.simulation.step, self.speed)
            future.add_done_callback(callback)

    def pause(self):
        logging.info('Pausing simulation')
        self.state = SimulationController.PAUSE

    def reset(self):
        self.canvas.delete('all')
        if self.state != SimulationController.PAUSE:
            self.pause()
        self.simulation.reset(self.start_population, self.food_count)
        self.initialize_canvas()

    def save(self):
        self.simulation.save()
