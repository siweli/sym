import tkinter as tk
from shitify import ui


if __name__== '__main__':
    root = tk.Tk()
    app = ui.AudioInterface(root)
    root.mainloop()