from application.application import Application
from models.simulation import Simulation

if __name__ == '__main__':
    application = Application(window_width=600, window_height=400)
    application.mainloop()
