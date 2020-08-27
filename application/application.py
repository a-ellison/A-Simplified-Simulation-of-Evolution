import tkinter
from application.simulation_controller import SimulationController
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle

DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 400
APPLICATION_TITLE = 'A Simplified Simulation of Evolution'
WIDGET_SPACING = 10


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
        self.canvas_width = self.window_width * 0.9
        self.canvas_height = self.window_height * 0.9
        self.canvas = tkinter.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.controls_frame = tkinter.Frame(self, height=200, width=150)
        self.play_simulation_button = tkinter.Button(self.controls_frame, text='Start Simulation',
                                                     command=self.play_simulation_action)
        self.pause_simulation_button = tkinter.Button(self.controls_frame, text='Pause Simulation',
                                                     command=self.pause_simulation_action)
        self.exit_button = tkinter.Button(self.controls_frame, text='Exit', command=self.exit_button_action)
        self.draw_widgets()
        self.simulation_controller = SimulationController(self)

    def configure_window(self):
        self.title(APPLICATION_TITLE)
        self.geometry(f'{self.window_width}x{self.window_height}')

    def play_simulation_action(self):
        self.simulation_controller.play()

    def pause_simulation_action(self):
        self.simulation_controller.pause()

    def exit_button_action(self):
        if self.simulation_controller.state == SimulationController.RUNNING:
            logging.info('Cant exit yet...')
            self.after(10, self.exit_button_action)
        else:
            logging.info('Exiting...')
            self.quit()

    def draw_widgets(self):
        self.canvas.place(x=self.window_width / 2 - self.canvas_width / 2, y=0)
        self.play_simulation_button.pack(side=tkinter.LEFT)
        self.pause_simulation_button.pack(side=tkinter.LEFT)
        self.exit_button.pack(side=tkinter.LEFT)
        self.controls_frame.place(x=self.window_width / 2 - 5 * WIDGET_SPACING,
                                  y=self.canvas_height + 3 * WIDGET_SPACING)
