import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shitify.themes import bg_colour_1, bg_colour_2, trim_colour

class WaveformDisplay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.fig = Figure(figsize=(4, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 100)
        self.line, = self.ax.plot(np.zeros(100))

        # set colours
        self.fig.patch.set_facecolor(bg_colour_1)
        self.ax.set_facecolor(bg_colour_2)
        self.line.set_color(trim_colour)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        # configure row/column expansion
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)




    def update_waveform(self, audio_data):
        """ Update waveform visualization """
        display_data = np.interp(
            np.linspace(0, len(audio_data) - 1, 100),
            np.arange(len(audio_data)),
            audio_data.flatten()
        )
        self.line.set_ydata(display_data)
        self.canvas.draw_idle()
