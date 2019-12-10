import logging
from tkinter import *

# Logging
logging.basicConfig(filename='actions.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')

window = Tk()
window.title('Hello World')
window.geometry('450x400')
window_width = 450
window_height = 400


# Circle using built-in oval function
def _create_circle(self, x, y, r, **kwargs):
    logging.debug('Create circle')
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


# Button actions
# Start simulation action
def start_sim_action():
    logging.info('Simulation started')
    last_action_label.config(text='Simulation started')


# Exit application action
def exit_action():
    logging.info('Exiting...')
    window.quit()


# Go to settings action
def setting_action():
    logging.info('Go to settings')
    last_action_label.config(text='Go to settings')


# Controls
# Frame containing controls
controlsFrame = Frame(window, height=200, width=150)
# Button to start simulation
start_sim_button = Button(controlsFrame, text='Start Simulation', command=start_sim_action)
# Setting button
setting_button = Button(controlsFrame, text='Settings', command=setting_action)
# Close window
exit_button = Button(controlsFrame, text='Exit', command=exit_action)
# Label with last action
last_action_label = Label(window, text='Click Something!')

# Canvas
canvas_side_length = 200
cv = Canvas(window, height=canvas_side_length, width=canvas_side_length, bg='black')
cv.create_circle(100, 100, 1, fill='blue')
cv.create_oval(100, 100, 1, 20, fill='blue')

# coord = 10, 50, 240, 210
# cv.create_arc(coord, start=0, extent=150, fill="red")

# Grid
# start_sim_button.grid(row=0, column=0, pady=10)
# setting_button.grid(row=0, column=1, pady=10)
# exit_button.grid(row=0, column=2, pady=10)
# last_action_label.grid(row=1, column=1)

cv.place(x=10, y=10)
start_sim_button.place(relx=0.1, rely=0.1)
setting_button.place(relx=0.1, rely=0.45)
exit_button.place(relx=0.1, rely=0.8)
controlsFrame.place(x=canvas_side_length + 20, y=10)
last_action_label.place(x=window_width/2-50, y=canvas_side_length+20)

window.mainloop()
