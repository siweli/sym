import tkinter as tk
import sys
import os
from PIL import Image, ImageTk, ImageSequence

class AnimatedGIF(tk.Label):
    def __init__(self, master, delay=100):
        super().__init__(master)

        # locate the resource and load it
        path = self.locate_resource()
        self.image = Image.open(path)
        self.frames = [
            ImageTk.PhotoImage(frame.copy().convert('RGBA'))
            for frame in ImageSequence.Iterator(self.image)
        ]
        self.delay = delay  # milliseconds between frames
        self.frame_index = 0
        self.animation_running = False

        # display the first frame by default
        self.config(image=self.frames[0])
        self.grid()




    def locate_resource(self):
        """ Go looking for the tense gif """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, 'tense.gif')




    def start(self):
        """ Start the animation if not already running """
        if not self.animation_running:
            self.animation_running = True
            self.animate()




    def animate(self):
        """ Run the GIF animation """
        if self.animation_running:
            self.config(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.after(self.delay, self.animate)




    def stop(self):
        """ Freeze the GIF on the first frame when paused """
        self.animation_running = False
        self.config(image=self.frames[0]) # reset to first frame
        self.frame_index = 0
