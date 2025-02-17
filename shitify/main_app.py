import tkinter as tk
import sounddevice as sd
import numpy as np
from shitify.ui import AudioInterface
from shitify.waveform import WaveformDisplay
from shitify.animated_gif import AnimatedGIF
from shitify.modifiers import loud_mic, downsample, reduce_bit_depth, add_static

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shitify Your Mic (sym)")
        self.geometry("900x500")

        # audio device settings
        self.input_device = 1
        self.output_device = 9
        self.samplerate = 44100

        # default everything to enabled except audio playback
        self.do_loud = True
        self.do_downsample = True
        self.do_reduce_depth = True
        self.do_static = True
        self.playback_enabled = False

        # default values for modifiers
        self.gain_value = 200
        self.downsample_rate = 8000
        self.upsample_rate = 44100
        self.bit_depth = 2

        # configure layout
        self.columnconfigure(0, weight=2) # for sliders
        self.columnconfigure(1, weight=1) # for audio visualizer and gif
        self.rowconfigure(0, weight=1) # audio visualizer on top
        self.rowconfigure(1, weight=1) # gif on bottom

        # UI Components
        self.audio_interface = AudioInterface(self)
        self.audio_interface.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.waveform_display = WaveformDisplay(self)
        self.waveform_display.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.animated_gif = AnimatedGIF(self, "tense.gif", 100)
        self.animated_gif.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # stream control
        self.stream = None
        self.create_stream_buttons()

        # audio playback toggle
        self.create_playback_toggle()


    ####################################################################################################################################
    # Start/stop the audio stream


    def create_stream_buttons(self):
        """ Creates buttons for starting and stopping the audio stream """
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        start_btn = tk.Button(btn_frame, text="Start Stream", command=self.start_stream)
        start_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(btn_frame, text="Stop Stream", command=self.stop_stream)
        stop_btn.pack(side=tk.LEFT, padx=5)




    def start_stream(self):
        """ Starts the microphone audio stream """
        if self.stream is None:
            self.stream = sd.Stream(
                channels=(1, 16),
                samplerate=self.samplerate,
                device=(self.input_device, self.output_device),
                callback=self.audio_callback
            )
            self.stream.start()
            self.audio_interface.status_label.config(text="Stream Running")




    def stop_stream(self):
        """ Stops the microphone audio stream """
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.audio_interface.status_label.config(text="Stream Stopped")


    ####################################################################################################################################
    # Audio callback


    def audio_callback(self, indata, outdata, frames, time, status):
        """ Processes live audio input and applies modifications """
        processed_audio = self.modify_audio(indata)
        outdata[:, 0] = processed_audio.flatten()

        # play the audio back if it is enabled
        if self.playback_enabled:
            sd.play(processed_audio, self.samplerate)

        # update the waveform display with the modified audio
        if hasattr(self, 'waveform_display'):
            self.waveform_display.update_waveform(processed_audio)

        # pause/play gif if the audio input is loud enough
        if hasattr(self, 'animated_gif'):
            if np.abs(indata).mean() > 0.05:
                self.animated_gif.start()
            else:
                self.animated_gif.stop()




    def modify_audio(self, audio):
        """ Applies the selected audio modifications """
        if self.do_loud:
            audio = loud_mic(audio, self.gain_value)
        if self.do_downsample:
            audio = downsample(audio, self.downsample_rate, self.upsample_rate)
        if self.do_reduce_depth:
            audio = reduce_bit_depth(audio, self.bit_depth)
        if self.do_static:
            audio = add_static(audio, intensity=0.2)
        return audio


    ####################################################################################################################################
    # Audio playback controls


    def create_playback_toggle(self):
        """ Creates a toggle button for enabling/disabling playback """
        self.playback_var = tk.BooleanVar(value=self.playback_enabled)
        playback_checkbox = tk.Checkbutton(
            self, text="Enable Playback",
            variable=self.playback_var, command=self.toggle_playback
        )
        playback_checkbox.grid(row=2, column=1, pady=10)




    def toggle_playback(self):
        """ Toggles audio playback on/off """
        self.playback_enabled = self.playback_var.get()
