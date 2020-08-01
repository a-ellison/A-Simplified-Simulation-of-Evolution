import concurrent.futures
import logging
from enum import Enum

from models.simulation import Simulation

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class SimulationController(object):
    STOP = 0
    GO = 1
    RUNNING = 2

    def __init__(self, app):
        self.app = app
        self.state = SimulationController.STOP
        self.simulation = Simulation(app.canvas_width, app.canvas_height)

    def update_canvas(self):
        # self.app.canvas.delete('all')
        # for animal in self.simulation.get_animals():
        #     self.draw_animal(animal)
        # self.app.canvas.update()
        logging.info('Updating canvas')

    def draw_animal(self, animal):
        point = animal.get_position()
        self.app.canvas.create_circle(point.x, point.y, animal.size, fill=animal.color.to_hex_string())

    def play(self):
        if self.state != SimulationController.RUNNING:
            logging.info('Simulation playing')
            self.state = SimulationController.RUNNING

            def callback(this_future):
                self.app.after(0, self.update_canvas)
                if self.state != SimulationController.STOP:
                    self.state = SimulationController.GO
                    self.play()

            future = thread_pool.submit(self.simulation.step)
            future.add_done_callback(callback)

    def pause(self):
        logging.info('Pausing simulation')
        self.state = SimulationController.STOP
