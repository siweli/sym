import tkinter as tk

class AudioInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # default everything to enabled
        self.do_gain = tk.BooleanVar(value=True)
        self.do_downsample = tk.BooleanVar(value=True)
        self.do_bit_depth = tk.BooleanVar(value=True)
        self.do_static = tk.BooleanVar(value=True)

        # default values for modifiers
        self.default_gain = 200
        self.default_bit_depth = 2
        self.default_static = 20 # (20%)
        self.default_downsample = 8000

        # build UI components
        self.build_ui()




    def build_ui(self):
        """ Creates UI sliders and toggle buttons for effects """
        self.grid(sticky="nsew")

        # create sliders
        self.create_gain_slider()
        self.create_bit_depth_slider()
        self.create_static_slider()
        self.create_downsample_slider()

        # stream status
        self.status_label = tk.Label(self, text="Stream Stopped", fg="#ff0000")
        self.status_label.pack(pady=10)



    def create_control_row(self, label_text, min_value, max_value, default_value, enabled_var):
        """
        Factory function that creates and returns a row containing:
            - A label with fixed width,
            - A horizontal slider (Scale) with the given min/max/default,
            - A text entry box showing the current value,
            - A checkbox to enable/disable the effect.

        The slider and entry are synchronized.
        """
        frame = tk.Frame(self)

        # Label with a fixed width so that all sliders line up
        label = tk.Label(frame, text=label_text, width=15, anchor="w")
        label.grid(row=0, column=0, sticky="w")

        # Slider with fixed length
        slider = tk.Scale(frame, from_=min_value, to=max_value, orient=tk.HORIZONTAL, length=200)
        slider.set(default_value)
        slider.grid(row=0, column=1, sticky="w", padx=(5, 5))

        # Entry widget to show the current value
        entry = tk.Entry(frame, width=6)
        entry.insert(0, str(default_value))
        entry.grid(row=0, column=2, padx=(5, 5))

        # Checkbox for enabling/disabling this effect
        checkbox = tk.Checkbutton(frame, text="Enable", variable=enabled_var)
        checkbox.grid(row=0, column=3, padx=(5, 5))

        # Callback: when slider moves, update the entry
        def slider_callback(value):
            try:
                val = int(float(value))
            except ValueError:
                val = default_value
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

        slider.config(command=slider_callback)

        # Callback: when entry is updated (Return or focus out), update the slider
        def entry_callback(event):
            try:
                new_value = int(entry.get())
            except ValueError:
                new_value = default_value
            # Snap to the slider's min and max if out-of-bounds
            new_value = max(min(new_value, max_value), min_value)
            slider.set(new_value)
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))

        entry.bind("<Return>", entry_callback)
        entry.bind("<FocusOut>", entry_callback)

        return frame, slider, entry, checkbox




    def create_gain_slider(self):
        """ Create gain slider """
        self.gain_frame, self.gain_slider, self.gain_entry, self.gain_checkbox = self.create_control_row(
            label_text="Gain:",
            min_value=1,
            max_value=1000,
            default_value=self.default_gain,
            enabled_var=self.do_gain
        )
        self.gain_frame.pack(pady=5, fill=tk.X)


    def create_bit_depth_slider(self):
        """ Create bit depth slider """
        self.bit_depth_frame, self.bit_depth_slider, self.bit_depth_entry, self.bit_depth_checkbox = self.create_control_row(
            label_text="Bit Depth:",
            min_value=1,
            max_value=16,
            default_value=self.default_bit_depth,
            enabled_var=self.do_bit_depth
        )
        self.bit_depth_frame.pack(pady=5, fill=tk.X)


    def create_static_slider(self):
        """ Create static slider """
        self.static_frame, self.static_slider, self.static_entry, self.static_checkbox = self.create_control_row(
            label_text="Static Intensity:",
            min_value=0,
            max_value=100,
            default_value=self.default_static,
            enabled_var=self.do_static
        )
        self.static_frame.pack(pady=5, fill=tk.X)


    def create_downsample_slider(self):
        """ Create downsample slider """
        self.downsample_frame, self.downsample_slider, self.downsample_entry, self.downsample_checkbox = self.create_control_row(
            label_text="Downsample Rate:",
            min_value=1000,
            max_value=44100,
            default_value=self.default_downsample,
            enabled_var=self.do_downsample
        )
        self.downsample_frame.pack(pady=5, fill=tk.X)


