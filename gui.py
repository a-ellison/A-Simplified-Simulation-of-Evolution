import logging
from tkinter import *

# Logging
log = open('actions.log')
logging.basicConfig(filename='converter.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


def start_sim_action():
    logging.info('Simulation started')
    test_label.config(text="Ich wurde geändert!")


def exit_action():
    logging.info('Exiting...')
    window.quit()


def setting_action():
    logging.info('Go to settings')
    last_action_label.config


window = Tk()
window.title("Ich mache nun was.")

# Button to start simulation
start_sim_button = Button(window, text="Start Simulation", command=start_sim_action)
# Setting button
setting_button = Button(window, text="Settings", command=setting_action)
# Close window
exit_button = Button(window, text="Exit", command=setting_action)

#
last_action_label = Label(window, text="Last action:\n\
...")

info_label = Label(window, text="Ich bin eine Info:\n\
Der Beenden Button schliesst das Programm.")

# Nun fügen wir die Komponenten unserem Fenster
# in der gwünschten Reihenfolge hinzu.
anweisungs_label.pack()
change_button.pack()
info_label.pack()
exit_button.pack()

# In der Ereignisschleife auf Eingabe des Benutzers warten.
window.mainloop()
