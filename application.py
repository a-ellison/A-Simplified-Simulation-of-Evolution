from tkinter import *
import world_controller
import logging

# Configure logging
logging.basicConfig(filename='application.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


APPLICATION_TITLE = 'A Simplified Simulation of Evolution'
WIDGET_SPACING = 10


class Application(object):
    def __init__(self, window_width=640, window_height=480, canvas_background_color='black', canvas_side_length=None):
        self.window_width = window_width
        self.window_height = window_height
        self.window = Tk()
        self.configure_window()

        if canvas_side_length is None:
            self.canvas_side_length = self.window_width / 2
        else:
            self.canvas_side_length = canvas_side_length
        self.canvas_background_color = canvas_background_color
        self.create_widgets()
        self.draw_graphic_elements()

        self.world_controller = world_controller.WorldController(self.canvas, self.canvas_side_length)

        self.window.after(100, self.run_world)
        self.window.mainloop()

    def configure_window(self):
        self.window.title(APPLICATION_TITLE)
        self.window.geometry(f'{self.window_width}x{self.window_height}')

    def create_widgets(self):
        self.canvas = Canvas(self.window, height=self.canvas_side_length, width=self.canvas_side_length,
                             bg=self.canvas_background_color)
        self.controls_frame = Frame(self.window, height=200, width=150)
        self.start_sim_button = Button(self.controls_frame, text='Start Simulation',
                                       command=self.start_simulation_button_action)
        self.setting_button = Button(self.controls_frame, text='Settings', command=self.settings_button_action)
        self.exit_button = Button(self.controls_frame, text='Exit', command=self.exit_button_action)
        self.last_action_label = Label(self.window, text='Click Something!')  # for testing

    def start_simulation_button_action(self):
        logging.info('Simulation started')
        self.last_action_label.config(text='Simulation started')  # for testing
        self.world_controller.start_simulation()

    def settings_button_action(self):
        logging.info('Go to settings')
        self.last_action_label.config(text='Go to settings')

    def exit_button_action(self):
        logging.info('Exiting...')
        self.window.quit()

    def draw_graphic_elements(self):
        self.last_action_label.place(x=self.window_width / 2 - 50, y=0)
        self.canvas.place(x=10, y=2*WIDGET_SPACING)
        # self.start_sim_button.place(relx=0.1, rely=0.1)
        self.start_sim_button.pack(side=LEFT)
        # self.setting_button.place(relx=0.1, rely=0.45)
        self.setting_button.pack(side=LEFT)
        # self.exit_button.place(relx=0.1, rely=0.8)
        self.exit_button.pack(side=LEFT)
        self.controls_frame.place(x=self.window_width/2, y=self.canvas_side_length + WIDGET_SPACING)

    def run_world(self):
        logging.debug('Run invoked')
        self.world_controller.run_world()
        self.window.after(100, self.run_world)

