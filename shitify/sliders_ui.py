import tkinter as tk

class AudioInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # build UI components
        self.build_ui()




    def build_ui(self):
        """ Creates UI sliders and toggle buttons for effects """
        self.grid(sticky="nsew")

        self.create_modifier_sliders()
        self.status_label = tk.Label(self, text="Stream Stopped", fg="blue")
        self.status_label.pack(pady=10)




    def create_modifier_sliders(self):
        """ Creates sliders to adjust effect parameters """
        frame = tk.Frame(self)
        frame.pack(pady=5)

        # gain slider
        self.gain_label = tk.Label(frame, text="Gain: 200")
        self.gain_label.pack()
        self.gain_slider = tk.Scale(frame, from_=0, to=1000, orient=tk.HORIZONTAL)
        self.gain_slider.set(200)
        self.gain_slider.pack()

        # bit depth slider
        self.bit_depth_label = tk.Label(frame, text="Bit Depth: 2")
        self.bit_depth_label.pack()
        self.bit_depth_slider = tk.Scale(frame, from_=2, to=16, orient=tk.HORIZONTAL)
        self.bit_depth_slider.set(2)
        self.bit_depth_slider.pack()

        # static checkbox
        self.static_var = tk.BooleanVar(value=False)
        static_checkbox = tk.Checkbutton(frame, text="Add Static", variable=self.static_var)
        static_checkbox.pack()
