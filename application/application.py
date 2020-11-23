import random
import time
import tkinter
from application.simulation_controller import SimulationController
import logging

from models import simulation

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')

random.seed(10)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle

DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
APPLICATION_TITLE = 'A Simplified Simulation of Evolution'
WIDGET_SPACING = 10

DEFAULT_START_POPULATION = 1
DEFAULT_FOOD_COUNT = 0
MAX_VALUE = 10000


# TODO: Restructure application to support
#  multiple pages and create pages for:
#   - data analysis
class Application(tkinter.Tk):
    def __init__(self, window_width=DEFAULT_WINDOW_WIDTH, window_height=DEFAULT_WINDOW_HEIGHT):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.configure_window()
        self.canvas_width = self.window_width * 0.7
        self.canvas_height = self.window_height * 0.7
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.controls_frame = tkinter.Frame(self)
        # Configuration
        self.speed_label = tkinter.Label(self.controls_frame, text='Speed:')
        self.speeds = tkinter.Frame(self.controls_frame)
        self.speed = tkinter.IntVar(value=simulation.Simulation.NORMAL)
        self.slow_radiobutton = tkinter.Radiobutton(self.speeds, text='Slow',
                                                    variable=self.speed, value=simulation.Simulation.SLOW)
        self.normal_radiobutton = tkinter.Radiobutton(self.speeds, text='Normal',
                                                      variable=self.speed, value=simulation.Simulation.NORMAL)
        self.fast_radiobutton = tkinter.Radiobutton(self.speeds, text='Fast',
                                                    variable=self.speed, value=simulation.Simulation.FAST)
        validate_entry = (self.register(self.is_valid_entry), '%P')
        self.seed = tkinter.IntVar(value=int(time.time()))
        self.seed_label = tkinter.Label(self.controls_frame, text='Random seed:')
        self.seed_entry = tkinter.Entry(self.controls_frame, width=10, textvariable=self.seed,
                                        validatecommand=validate_entry, command=self.set_seed)
        self.start_population_label = tkinter.Label(self.controls_frame, text='Start Population:')
        self.start_population = tkinter.IntVar(value=DEFAULT_START_POPULATION)
        self.start_population_spinbox = tkinter.Spinbox(self.controls_frame, from_=0, to=MAX_VALUE, increment=5,
                                                        width=5, textvariable=self.start_population, validate='key',
                                                        validatecommand=validate_entry)
        self.food_count_label = tkinter.Label(self.controls_frame, text='Food Count:')
        self.food_count = tkinter.IntVar(value=DEFAULT_FOOD_COUNT)
        self.food_count_spinbox = tkinter.Spinbox(self.controls_frame, from_=0, to=MAX_VALUE, increment=5, width=5,
                                                  textvariable=self.food_count, validate='key',
                                                  validatecommand=validate_entry)
        self.simulation_controller = SimulationController(self.canvas, self.canvas_width, self.canvas_height, self.speed, self.seed,
                                                          self.start_population, self.food_count)
        # Control
        self.play_pause_simulation_button = tkinter.Button(self.controls_frame, text='Play/Pause',
                                                           command=self.play_pause_action)
        self.reset_simulation_button = tkinter.Button(self.controls_frame, text='Reset',
                                                      command=self.simulation_controller.reset)
        self.exit_button = tkinter.Button(self.controls_frame, text='Exit', command=self.exit_action)
        self.set_keybinds()
        self.place_widgets()

    def configure_window(self):
        self.title(APPLICATION_TITLE)
        self.geometry(f'{self.window_width}x{self.window_height}')

    def set_seed(self):
        random.seed(self.seed.get())

    def play_pause_action(self, *args):
        if self.simulation_controller.state == SimulationController.PAUSE:
            self.simulation_controller.play()
            logging.info('Playing simulation')
        else:
            self.simulation_controller.pause()
            logging.info('Pausing simulation')

    @classmethod
    def is_valid_entry(cls, new_value):
        return new_value.isdigit() and 0 <= int(new_value)

    def exit_action(self, *args):
        if self.simulation_controller.state == SimulationController.RUNNING:
            logging.info('Can\'t exit yet...')
            self.simulation_controller.pause()
            self.after(50, self.exit_action)
        else:
            self.simulation_controller.save()
            logging.info('Exiting...')
            self.quit()

    def set_keybinds(self):
        self.bind('<space>', self.play_pause_action)
        self.bind('<e>', self.exit_action)
        self.bind('<r>', lambda *args: self.simulation_controller.reset())

    def place_widgets(self):
        self.canvas.place(x=self.window_width / 2 - self.canvas_width / 2, y=0)
        self.play_pause_simulation_button.grid(column=0, row=0, rowspan=2)
        self.reset_simulation_button.grid(column=1, row=0, rowspan=2)
        self.exit_button.grid(column=2, row=0, rowspan=2)
        self.speed_label.grid(column=3, row=0)
        self.slow_radiobutton.pack(anchor=tkinter.W)
        self.normal_radiobutton.pack(anchor=tkinter.W)
        self.fast_radiobutton.pack(anchor=tkinter.W)
        self.speeds.grid(column=3, row=1)
        self.seed_label.grid(column=4, row=0)
        self.seed_entry.grid(column=4, row=1)
        self.start_population_label.grid(column=0, row=3)
        self.start_population_spinbox.grid(column=0, row=4)
        self.food_count_label.grid(column=1, row=3)
        self.food_count_spinbox.grid(column=1, row=4)
        self.controls_frame.place(x=WIDGET_SPACING, y=self.canvas_height + WIDGET_SPACING)
