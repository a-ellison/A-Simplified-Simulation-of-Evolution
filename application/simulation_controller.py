import concurrent.futures
import tkinter

from models.simulation import Simulation

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)


class SimulationController(object):
    PAUSE = 0
    PLAY = 1
    RUNNING = 2

    def __init__(self, canvas: tkinter.Canvas, canvas_width, canvas_height, start_population, food_count):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.state = SimulationController.PAUSE
        self.speed = 1
        self.start_population = start_population
        self.food_count = food_count
        self.simulation = Simulation(self.canvas_width, self.canvas_height, start_population, food_count)
        self.update_canvas()

    def update_canvas(self):
        all_canvas_ids = list(self.canvas.find_all())
        for drawable in self.simulation.all_drawables:
            if drawable.canvas_id is None:
                drawable.canvas_id = self.canvas.create_circle(drawable.position.x, drawable.position.y, drawable.radius,
                                                               fill=drawable.color.to_hex())
            else:
                dx = drawable.position.x - drawable.last_position.x
                dy = drawable.position.y - drawable.last_position.y
                self.canvas.move(drawable.canvas_id, dx, dy)
                all_canvas_ids.remove(drawable.canvas_id)
        for unused in all_canvas_ids:
            self.canvas.delete(unused)
        self.canvas.update()

    def play(self):
        if self.state != SimulationController.RUNNING:
            self.state = SimulationController.RUNNING

            def callback(this_future):
                if this_future._result == Simulation.ERROR:
                    raise BaseException('An error has ocurred: ' + str(this_future._exception))
                elif this_future._result == Simulation.FINISHED:
                    self.pause()
                    self.show_message('The simulation has finished')
                else:
                    self.update_canvas()
                    if self.state != SimulationController.PAUSE:
                        self.state = SimulationController.PLAY
                        self.play()

            future = thread_pool.submit(self.simulation.step, self.speed)
            # future = thread_pool.submit(self.simulation.step, self.speed, 0.1)
            future.add_done_callback(callback)

    def pause(self):
        self.state = SimulationController.PAUSE

    def reset(self):
        self.canvas.delete('all')
        if self.state != SimulationController.PAUSE:
            self.pause()
        self.simulation.reset(self.start_population, self.food_count)
        self.update_canvas()

    def save(self):
        self.simulation.save()

    def show_message(self, msg):
        self.canvas.delete('all')
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, fill='white', text=msg)
