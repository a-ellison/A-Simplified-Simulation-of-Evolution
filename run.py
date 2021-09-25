from application.application import Application
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

if __name__ == "__main__":
    application = Application()
    application.mainloop()
