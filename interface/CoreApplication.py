import tkinter as Tkinter

class CoreApplication(Tkinter.Tk):
    def __init__(self):
        super(CoreApplication, self).__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        print("Closing the application...")
        self.destroy()