import concurrent.futures
import logging
import time

from models.simulation import Simulation

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class SimulationController(object):
    PAUSE = 0
    PLAY = 1
    RUNNING = 2

    def __init__(self, canvas):
        self.canvas = canvas
        self.state = SimulationController.PAUSE
        self.simulation = Simulation(self.canvas.master.canvas_width, self.canvas.master.canvas_height)
        self.initialize_canvas()

    def initialize_canvas(self):
        for drawable in self.simulation.get_all_drawables():
            canvas_object = self.canvas.create_circle(drawable.x, drawable.y, drawable.size, fill=drawable.color.to_hex())
            drawable.canvas_object = canvas_object

    def update_canvas(self):
        for drawable in self.simulation.get_all_drawables():
            dx = drawable.x - drawable.last_x
            dy = drawable.y - drawable.last_y
            self.canvas.move(drawable.canvas_object, dx, dy)
        self.canvas.update()

    def play(self):
        if self.state != SimulationController.RUNNING:
            self.state = SimulationController.RUNNING

            def callback(this_future):
                if not this_future._result:
                    raise BaseException('An error has ocurred: ' + str(this_future._exception))
                self.update_canvas()
                if self.state != SimulationController.PAUSE:
                    self.state = SimulationController.PLAY
                    self.play()

            future = thread_pool.submit(self.simulation.step)
            future.add_done_callback(callback)

    def pause(self):
        logging.info('Pausing simulation')
        self.state = SimulationController.PAUSE

