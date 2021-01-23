import logging
import tkinter

from application.simulation_controller import SimulationController
from helpers import Speed, State
from models.simulation import Behaviors

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


tkinter.Canvas.create_circle = _create_circle

DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 400
APPLICATION_TITLE = "A Simplified Simulation of Evolution"
WIDGET_SPACING = 10

DEFAULT_SPINBOX = {"to": 10000, "width": 5, "increment": 5, "validate": "key"}


class Application(tkinter.Tk):
    def __init__(
        self, window_width=DEFAULT_WINDOW_WIDTH, window_height=DEFAULT_WINDOW_HEIGHT
    ):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.configure_window()
        self.canvas_width = self.window_width * 0.7
        self.canvas_height = self.window_height * 0.7
        self.canvas = tkinter.Canvas(
            self, width=self.canvas_width, height=self.canvas_height, bg="black"
        )
        self.meta_frame = tkinter.Frame(self)
        self.controls_frame = tkinter.Frame(self.meta_frame)
        self.behavior = tkinter.StringVar(value=Behaviors.PRIMER.name)
        choices = [e.name for e in list(Behaviors)]
        # does reset if option selected
        self.behaviors = tkinter.OptionMenu(
            self.controls_frame, self.behavior, *choices, command=self.model_changed
        )
        self.speed_label = tkinter.Label(self.controls_frame, text="Speed:")
        self.speeds = tkinter.Frame(self.controls_frame)
        self.speed = tkinter.IntVar(value=Speed.NORMAL.value)
        self.slow_radiobutton = tkinter.Radiobutton(
            self.speeds, text="Slow", variable=self.speed, value=Speed.SLOW.value
        )
        self.normal_radiobutton = tkinter.Radiobutton(
            self.speeds, text="Normal", variable=self.speed, value=Speed.NORMAL.value
        )
        self.fast_radiobutton = tkinter.Radiobutton(
            self.speeds, text="Fast", variable=self.speed, value=Speed.FAST.value
        )
        self.seed_label = tkinter.Label(self.controls_frame, text="Random seed:")
        self.seed = tkinter.StringVar(value="")
        validate_seed = (self.register(self.is_valid_seed), "%P")
        self.seed_entry = tkinter.Entry(
            self.controls_frame,
            width=10,
            textvariable=self.seed,
            validate="key",
            validatecommand=validate_seed,
        )
        self.play_pause_simulation_button = tkinter.Button(
            self.controls_frame, text="Play/Pause", command=self.play_pause_action
        )
        self.reset_simulation_button = tkinter.Button(
            self.controls_frame, text="Reset", command=self.reset_action
        )
        self.exit_button = tkinter.Button(
            self.controls_frame, text="Exit", command=self.exit_action
        )
        self.simulation_controller = SimulationController(
            self.canvas,
            self.canvas_width,
            self.canvas_height,
            self.behavior,
            self.speed,
            self.seed,
        )
        self.params_frame = tkinter.Frame(self.meta_frame)
        self.simulation_controller.params = self.create_param_widgets()
        self.simulation_controller.setup()
        self.place_widgets()
        self.set_keybinds()

    def configure_window(self):
        self.title(APPLICATION_TITLE)
        self.geometry(f"{self.window_width}x{self.window_height}")

    def play_pause_action(self, *args):
        if self.simulation_controller.state == State.PAUSE:
            self.simulation_controller.play()
            logging.info("Playing simulation")
        else:
            self.simulation_controller.pause()
            logging.info("Pausing simulation")

    @classmethod
    def is_valid_entry(cls, new_value):
        return new_value.isdigit() and 0 <= int(new_value)

    @classmethod
    def is_valid_seed(cls, new_value):
        return new_value == "" or cls.is_valid_entry(new_value)

    @classmethod
    def validate_param(cls, new_value):
        if cls.is_valid_entry(new_value):
            return True
        return False

    def param_updated(self, *args):
        self.simulation_controller.update_config()

    def reset_action(self, *args):
        self.simulation_controller.setup()

    def exit_action(self, *args):
        if self.simulation_controller.state == State.RUNNING:
            logging.info("Can't exit yet...")
            self.simulation_controller.pause()
            self.after(50, self.exit_action)
        else:
            self.simulation_controller.save()
            logging.info("Exiting...")
            self.quit()

    def model_changed(self, *args):
        self.clear_param_widgets()
        self.simulation_controller.params = self.create_param_widgets()
        self.reset_action()

    def clear_param_widgets(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()

    def set_keybinds(self):
        self.bind("<space>", self.play_pause_action)
        self.bind("<e>", self.exit_action)
        self.bind("<r>", self.reset_action)
        self.bind(
            "<k>",
            lambda *args: self.speed.set(Speed(self.speed.get()).reduce().value),
        )
        self.bind(
            "<j>",
            lambda *args: self.speed.set(Speed(self.speed.get()).increment().value),
        )

    def create_param_widgets(self):
        config = Behaviors[self.behavior.get()].value.get_config()
        params = {}
        count = 0
        for key in config:
            param = config[key]
            if param.get("type", "entry") == "radio":
                var = self.create_radio_param(param, count)
            else:
                var = self.create_entry_param(param, count)
            params[key] = var
            count += 1
        return params

    def create_radio_param(self, param, count):
        options = param.get("options", ["empty"])
        label = tkinter.Label(self.params_frame, text=param.get("label", ""))
        radio_var = tkinter.StringVar(value=options[0])
        radio_frame = tkinter.Frame(self.params_frame)
        for option in options:
            radio = tkinter.Radiobutton(
                radio_frame,
                text=option,
                variable=radio_var,
                value=option,
                command=self.param_updated,
            )
            radio.pack(anchor=tkinter.W)
        label.grid(column=count, row=0)
        radio_frame.grid(column=count, row=1)
        return radio_var

    def create_entry_param(self, param, count):
        label = tkinter.Label(self.params_frame, text=param.get("label", ""))
        var = tkinter.IntVar(value=param.get("default", 0))
        var.trace("w", self.param_updated)
        validate = (self.register(self.is_valid_entry), "%P")
        entry = tkinter.Spinbox(
            self.params_frame,
            from_=0,
            textvariable=var,
            validatecommand=validate,
            **DEFAULT_SPINBOX,
        )
        label.grid(column=count, row=0)
        entry.grid(column=count, row=1)
        return var

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
