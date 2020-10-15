import tkinter
from application.simulation_controller import SimulationController
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle

DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600
APPLICATION_TITLE = 'A Simplified Simulation of Evolution'
WIDGET_SPACING = 10

DEFAULT_START_POPULATION = 100
DEFAULT_FOOD_COUNT = 75
MAX_VALUE = 10000


# TODO: Restructure application to support
#  multiple pages and create pages for:
#   - settings
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
        self.controls_frame = tkinter.Frame(self, height=200, width=150)
        self.simulation_controller = SimulationController(self.canvas, DEFAULT_START_POPULATION, DEFAULT_FOOD_COUNT)
        self.play_simulation_button = tkinter.Button(self.controls_frame, text='Play',
                                                     command=self.simulation_controller.play)
        self.pause_simulation_button = tkinter.Button(self.controls_frame, text='Pause',
                                                      command=self.simulation_controller.pause)
        self.reset_simulation_button = tkinter.Button(self.controls_frame, text='Reset',
                                                      command=self.reset_simulation_action)
        self.exit_button = tkinter.Button(self.controls_frame, text='Exit', command=self.exit_button_action)
        self.speed_label = tkinter.Label(self.controls_frame, text='Speed:')
        self.speed = tkinter.IntVar(value=1)
        self.speed_scale = tkinter.Scale(self.controls_frame, variable=self.speed, from_=1, to=10,
                                         command=self.speed_scale_action, orient=tkinter.HORIZONTAL)
        self.start_population_label = tkinter.Label(self.controls_frame, text='Start Population:')
        validate_entry_command = (self.register(self.validate_entry), '%P')
        self.start_population = tkinter.IntVar(value=DEFAULT_START_POPULATION)
        self.start_population_spinbox = tkinter.Spinbox(self.controls_frame, from_=1, to=MAX_VALUE, increment=5,
                                                        width=5, textvariable=self.start_population, validate='key',
                                                        validatecommand=validate_entry_command)
        self.food_count_label = tkinter.Label(self.controls_frame, text='Food Count:')
        self.food_count = tkinter.IntVar(value=DEFAULT_FOOD_COUNT)
        self.food_count_spinbox = tkinter.Spinbox(self.controls_frame, from_=1, to=MAX_VALUE, increment=5, width=5,
                                                  textvariable=self.food_count, validate='key',
                                                  validatecommand=validate_entry_command)
        self.place_widgets()

    def configure_window(self):
        self.title(APPLICATION_TITLE)
        self.geometry(f'{self.window_width}x{self.window_height}')

    def play_simulation_action(self):
        self.simulation_controller.play()

    def reset_simulation_action(self):
        self.canvas.delete('all')
        if not self.simulation_controller.PAUSE:
            self.simulation_controller.pause()
        self.simulation_controller = SimulationController(self.canvas, self.start_population.get(),
                                                          self.food_count.get())

    @classmethod
    def validate_entry(cls, new_value):
        return new_value.isdigit() and 0 < int(new_value) <= MAX_VALUE

    def exit_button_action(self):
        if self.simulation_controller.state == SimulationController.RUNNING:
            logging.info('Can\'t exit yet...')
            self.simulation_controller.pause()
            self.after(50, self.exit_button_action)
        else:
            logging.info('Exiting...')
            self.quit()

    def speed_scale_action(self, new_speed):
        self.simulation_controller.speed = self.speed_scale.get()

    def place_widgets(self):
        self.canvas.place(x=self.window_width / 2 - self.canvas_width / 2, y=0)
        self.play_simulation_button.grid(column=0, row=0, rowspan=2)
        self.pause_simulation_button.grid(column=1, row=0, rowspan=2)
        self.reset_simulation_button.grid(column=2, row=0, rowspan=2)
        self.exit_button.grid(column=3, row=0, rowspan=2)
        self.speed_label.grid(column=4, row=0)
        self.speed_scale.grid(column=4, row=1)
        self.start_population_label.grid(column=5, row=0)
        self.start_population_spinbox.grid(column=5, row=1)
        self.food_count_label.grid(column=6, row=0)
        self.food_count_spinbox.grid(column=6, row=1)
        self.controls_frame.place(x=WIDGET_SPACING,
                                  y=self.canvas_height + WIDGET_SPACING)
