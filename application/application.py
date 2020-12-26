import tkinter
from application.simulation_controller import SimulationController
import logging

from helpers import Speed, State
from models.simulation import Behaviors

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle

DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
APPLICATION_TITLE = 'A Simplified Simulation of Evolution'
WIDGET_SPACING = 10

DEFAULT_SPINBOX = {
    'to': 10000,
    'width': 5,
    'increment': 5,
    'validate': 'key'
}


class Application(tkinter.Tk):
    def __init__(self, window_width=DEFAULT_WINDOW_WIDTH, window_height=DEFAULT_WINDOW_HEIGHT):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.configure_window()
        self.canvas_width = self.window_width * 0.7
        self.canvas_height = self.window_height * 0.7
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.meta_frame = tkinter.Frame(self)
        self.controls_frame = tkinter.Frame(self.meta_frame)
        self.behavior = tkinter.StringVar(value=Behaviors.PRIMER.name)
        choices = [e.name for e in list(Behaviors)]
        self.behaviors = tkinter.OptionMenu(self.controls_frame, self.behavior, *choices)
        self.speed_label = tkinter.Label(self.controls_frame, text='Speed:')
        self.speeds = tkinter.Frame(self.controls_frame)
        self.speed = tkinter.IntVar(value=Speed.NORMAL.value)
        self.slow_radiobutton = tkinter.Radiobutton(self.speeds, text='Slow',
                                                    variable=self.speed, value=Speed.SLOW.value)
        self.normal_radiobutton = tkinter.Radiobutton(self.speeds, text='Normal',
                                                      variable=self.speed, value=Speed.NORMAL.value)
        self.fast_radiobutton = tkinter.Radiobutton(self.speeds, text='Fast',
                                                    variable=self.speed, value=Speed.FAST.value)
        self.seed_label = tkinter.Label(self.controls_frame, text='Random seed:')
        self.seed = tkinter.StringVar(value='')
        validate_seed = (self.register(self.is_valid_seed), '%P')
        self.seed_entry = tkinter.Entry(self.controls_frame, width=10, textvariable=self.seed, validate='key',
                                        validatecommand=validate_seed)
        self.params_frame = tkinter.Frame(self.meta_frame)
        self.params = self.create_parameter_widgets()
        self.simulation_controller = SimulationController(self.canvas, self.canvas_width, self.canvas_height,
                                                          self.behavior, self.speed, self.seed, self.params)
        self.play_pause_simulation_button = tkinter.Button(self.controls_frame, text='Play/Pause',
                                                           command=self.play_pause_action)
        self.reset_simulation_button = tkinter.Button(self.controls_frame, text='Reset',
                                                      command=self.simulation_controller.setup)
        self.exit_button = tkinter.Button(self.controls_frame, text='Exit', command=self.exit_action)
<<<<<<< HEAD
        self.speed_label = tkinter.Label(self.controls_frame, text='Speed:')
        self.speed = tkinter.IntVar(value=1)
        self.speed_scale = tkinter.Scale(self.controls_frame, variable=self.speed, from_=1, to=100,
                                         command=self.set_speed_action, orient=tkinter.HORIZONTAL)
        self.start_population_label = tkinter.Label(self.controls_frame, text='Start Population:')
        self.start_population = tkinter.IntVar(value=DEFAULT_START_POPULATION)
        validate_start_population = (self.register(self.validate_start_population), '%P')
        self.start_population_spinbox = tkinter.Spinbox(self.controls_frame, from_=0, to=MAX_VALUE, increment=5,
                                                        width=5, textvariable=self.start_population, validate='key',
                                                        validatecommand=validate_start_population)
        self.food_count_label = tkinter.Label(self.controls_frame, text='Food Count:')
        self.food_count = tkinter.IntVar(value=DEFAULT_FOOD_COUNT)
        validate_food_count = (self.register(self.validate_food_count), '%P')
        self.food_count_spinbox = tkinter.Spinbox(self.controls_frame, from_=0, to=MAX_VALUE, increment=5, width=5,
                                                  textvariable=self.food_count, validate='key',
                                                  validatecommand=validate_food_count)
        self.seed = -1
        validate_seed = (self.register(self.validate_seed), '%P')
        self.seed_spinbox = tkinter.Entry(self.controls_frame, width=5, textvariable=self.seed,
                                          validatecommand=validate_seed)
        self.set_keybinds()
=======
>>>>>>> origin/master
        self.place_widgets()
        self.set_keybinds()

    def configure_window(self):
        self.title(APPLICATION_TITLE)
        self.geometry(f'{self.window_width}x{self.window_height}')

    def play_pause_action(self, *args):
        if self.simulation_controller.state == State.PAUSE:
            self.simulation_controller.play()
            logging.info('Playing simulation')
        else:
            self.simulation_controller.pause()
            logging.info('Pausing simulation')

    @classmethod
    def is_valid_entry(cls, new_value):
        return new_value.isdigit() and 0 <= int(new_value)

    @classmethod
    def is_valid_seed(cls, new_value):
        return new_value == '' or cls.is_valid_entry(new_value)

    def exit_action(self, *args):
        if self.simulation_controller.state == State.RUNNING:
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
        self.bind('<r>', lambda *args: self.simulation_controller.setup())

    def create_parameter_widgets(self):
        config = Behaviors[self.behavior.get()].value.params()
        validate = (self.register(self.is_valid_entry), '%P')
        params = {}
        count = 0
        for key in config:
            param = config[key]
            label = tkinter.Label(self.params_frame, text=param.get('label', ''))
            var = tkinter.IntVar(value=param.get('default', 0))
            entry = tkinter.Spinbox(self.params_frame, from_=0, textvariable=var, validatecommand=validate, **DEFAULT_SPINBOX)
            params[key] = var
            label.grid(column=count, row=0)
            entry.grid(column=count, row=1)
            count += 1
        return params

    def place_widgets(self):
        self.canvas.place(x=self.window_width / 2 - self.canvas_width / 2, y=0)
        self.play_pause_simulation_button.grid(column=0, row=0, rowspan=2)
        self.reset_simulation_button.grid(column=1, row=0, rowspan=2)
        self.exit_button.grid(column=2, row=0, rowspan=2)
        self.behaviors.grid(column=3, row=0, rowspan=2)
        self.speed_label.grid(column=4, row=0)
        self.slow_radiobutton.pack(anchor=tkinter.W)
        self.normal_radiobutton.pack(anchor=tkinter.W)
        self.fast_radiobutton.pack(anchor=tkinter.W)
        self.speeds.grid(column=4, row=1)
        self.seed_label.grid(column=5, row=0)
        self.seed_entry.grid(column=5, row=1)
        self.controls_frame.grid(column=0, row=0)
        self.params_frame.grid(column=0, row=1)
        self.meta_frame.place(x=WIDGET_SPACING, y=self.canvas_height + WIDGET_SPACING)

    def reset_params(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.params = self.create_parameter_widgets()
