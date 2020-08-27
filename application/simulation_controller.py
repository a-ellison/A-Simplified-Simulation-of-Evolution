import concurrent.futures
import logging

from models.simulation import Simulation

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class SimulationController(object):
    PAUSE = 0
    PLAY = 1
    RUNNING = 2

    def __init__(self, canvas, canvas_width, canvas_height):
        self.canvas = canvas
        self.state = SimulationController.PAUSE
        self.simulation = Simulation(canvas_width, canvas_height)

    def update_canvas(self):
        self.canvas.delete('all')
        for obj in self.simulation.get_all_objects():
            self.draw(obj)
        self.canvas.update()

    def draw(self, obj):
        self.canvas.create_circle(obj.x, obj.y, obj.size, fill=obj.color.to_hex())

    def play(self):
        if self.state != SimulationController.RUNNING:
            logging.info('Not running right now --> playing simulation')
            self.state = SimulationController.RUNNING

            def callback(this_future):
                self.canvas.after(0, self.update_canvas)
                if self.state != SimulationController.PAUSE:
                    self.state = SimulationController.PLAY
                    self.play()

            future = thread_pool.submit(self.simulation.step)
            future.add_done_callback(callback)

    def pause(self):
        logging.info('Pausing simulation')
        self.state = SimulationController.PAUSE
