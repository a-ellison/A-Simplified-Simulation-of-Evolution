import logging
import time

from helpers import ThreadPoolExecutorStackTraced, State, Speed
from models.simulation import Simulation, Behaviors
from structs.point import Point

thread_pool = ThreadPoolExecutorStackTraced(max_workers=1)


class SimulationController(object):
    def __init__(self, canvas, canvas_width, canvas_height, behavior_var, speed_var, seed_var):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.behavior_var = behavior_var
        self.speed_var = speed_var
        self.seed_var = seed_var
        self.state = State.PAUSE
        self.simulation = None
        self.params = {}
        self._setup = False
        self.canvas.after(17, self.canvas_refresh)

    def update_canvas(self):
        all_canvas_ids = list(self.canvas.find_all())
        for drawable in self.simulation.all_drawables:
            if drawable.canvas_id is None:
                drawable.canvas_id = self.canvas.create_circle(drawable.position.x, drawable.position.y,
                                                               drawable.radius,
                                                               fill=drawable.color.to_hex())
            else:
                dx = drawable.position.x - drawable.last_drawn_position.x
                dy = drawable.position.y - drawable.last_drawn_position.y
                if dx or dy:
                    self.canvas.move(drawable.canvas_id, dx, dy)
                drawable.last_drawn_position = Point(drawable.position.x, drawable.position.y)
                all_canvas_ids.remove(drawable.canvas_id)
        for unused in all_canvas_ids:
            self.canvas.delete(unused)
        self.canvas.update()

    def canvas_refresh(self):
        if self.state != State.PAUSE:
            self.update_canvas()
        self.canvas.after(17, self.canvas_refresh)

    def play(self):
        if self.state != State.RUNNING:
            self.state = State.RUNNING

            def callback(this_future):
                # TODO: this block is unnecessary the way it is ATM
                try:
                    result = this_future.result()
                except Exception:
                    raise
                if result == State.FINISHED:
                    self.pause()
                    self.show_message('The simulation has finished')
                else:
                    if self.state != State.PAUSE:
                        self.state = State.PLAY
                        self.play()

            future = thread_pool.submit(self.simulation.step, Speed(self.speed_var.get()))
            future.add_done_callback(callback)

    def pause(self):
        self.state = State.PAUSE

    def setup(self):
        self._setup = True
        self.canvas.delete('all')
        if self.state != State.PAUSE:
            self.pause()
        behavior = Behaviors[self.behavior_var.get()].value
        self.simulation = Simulation(self.canvas_width, self.canvas_height, behavior, self.seed, self.config)
        self.update_canvas()

    @property
    def seed(self):
        if self.seed_var.get() == '':
            # more or less unique time
            seed = int((time.time() * 10 ** 4) % 10 ** 7)
        else:
            seed = int(self.seed_var.get())
        return seed

    @property
    def config(self):
        return {k: v.get() for k, v in self.params.items()}

    def update_config(self):
        if self._setup:
            self.simulation.update_config(self.config)

    def save(self):
        self.simulation.save()

    def show_message(self, msg):
        self.canvas.delete('all')
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, fill='white', text=msg)
