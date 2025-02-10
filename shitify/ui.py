import tkinter as tk
import sounddevice as sd
from shitify.modifiers import loud_mic, downsample, reduce_bit_depth



class AudioInterface:
    def __init__(self, master):
        self.m = master
        master.title("Shitify Your Mic (sym)")

        # default audio stream settings
        self.stream = None
        self.input_device = 1
        self.output_device = 9
        self.do_loud = True
        self.do_downsample = True
        self.do_reduce_depth = True

        # default audio modifier values
        self.gain_value = 200
        self.downsample_rate = 8000
        self.upsample_rate = 44100
        self.bit_depth = 2

        # build the user interface
        self.build_ui()

        # Ensure proper cleanup on close
        master.protocol("WM_DELETE_WINDOW", self.on_closing)


    ################################################################################
    # Handle the audio stream starting and stopping


    def on_closing(self):
        # cleanup on close
        self.stop_stream()
        self.m.destroy()



    def start_stream(self):
        # start audio stream
        self.stream = sd.Stream(
            channels=(1, 16),
            samplerate=44100,
            device=(
                self.input_device,
                self.output_device
            ),
            callback=self.callback
        )
        self.stream.start()

        # Update the status label accordingly:
        self.status_label.config(text="Stream Running")



    def stop_stream(self):
        # stop audio stream if it is running
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.status_label.config(text="Stream Stopped")


    ################################################################################
    # Real time audio modifier


    # real time processing
    def callback(self, indata, outdata, frames, time, status):
        # change the audio in real time
        processed_audio = self.modify_audio(indata)

        # outdata[:] = np.tile(processed_audio, (1, 16))
        outdata[:, 0] = processed_audio.flatten()



    def modify_audio(self, audio):
        if self.do_loud is True:
            audio = loud_mic(audio, self.gain_value)
        if self.do_downsample is True:
            audio = downsample(audio, self.downsample_rate, self.upsample_rate)
        if self.do_reduce_depth is True:
            audio = reduce_bit_depth(audio, self.bit_depth)
        return audio


    ################################################################################
    # Build the UI


    def toggle_stream(self):
        # --- Build the UI ---
        # Buttons for controlling the stream
        self.start_button = tk.Button(self.m, text="Start Stream", command=self.start_stream)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(self.m, text="Stop Stream", command=self.stop_stream)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)



    def audio_disruptors(self):
        # frame for the sliders
        frame = tk.Frame(self.m)
        frame.grid(row=1, column=0, padx=5, pady=5)

        # gain slider
        self.gain_label = tk.Label(frame, text=f"Gain: {self.gain_value}")
        self.gain_label.grid(row=0, column=0, padx=5, pady=5)

        self.gain_slider = tk.Scale(frame, from_=0, to=500, orient=tk.HORIZONTAL, command=self.update_gain)
        self.gain_slider.set(self.gain_value)
        self.gain_slider.grid(row=0, column=1, padx=5, pady=5)


        # Bit Depth slider
        self.bit_depth_label = tk.Label(frame, text=f"Bit Depth: {self.bit_depth}")
        self.bit_depth_label.grid(row=1, column=0, padx=5, pady=5)

        self.bit_depth_slider = tk.Scale(frame, from_=2, to=16, orient=tk.HORIZONTAL, command=self.update_bit_depth)
        self.bit_depth_slider.set(self.bit_depth)
        self.bit_depth_slider.grid(row=1, column=1, padx=5, pady=5)



    def build_ui(self):
        # build functions
        self.toggle_stream()
        self.audio_disruptors()

        # Status label for stream state or errors
        self.status_label = tk.Label(self.m, text="Stream Stopped", fg="blue")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=10)



    def update_gain(self, value):
        # Update the gain parameter (you may need to update a global or shared variable)
        self.gain_value = float(value)
        self.gain_label.config(text=f"Gain: {self.gain_value}")

    def update_bit_depth(self, value):
        # Update the bit depth parameter
        self.bit_depth_value = int(value)
        self.bit_depth_label.config(text=f"Bit Depth: {self.bit_depth_value}")