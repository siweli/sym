import tkinter as tk
import sounddevice as sd
import numpy as np
from collections import deque
from shitify.sliders_ui import AudioInterface
from shitify.waveform import WaveformDisplay
from shitify.animated_gif import AnimatedGIF
from shitify.modifiers import loud_mic, downsample, reduce_bit_depth, add_static
from shitify.themes import bg_colour_1, fg_colour

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shitify Your Mic (sym)")
        self.geometry("900x500")

        # audio device settings
        self.input_device = 1
        self.output_device = 9
        self.samplerate = 44100

        # configure layout
        self.columnconfigure(0, weight=2) # for sliders
        self.columnconfigure(1, weight=1) # for audio visualizer and gif
        self.rowconfigure(0, weight=1) # audio visualizer on top
        self.rowconfigure(1, weight=1) # gif on bottom

        # set colours
        self.configure(bg=bg_colour_1)
        self.option_add("*Background", bg_colour_1)
        self.option_add("*Foreground", fg_colour)

        # self.option_add("*Button.Background", bg_colour_1)
        self.option_add("*Button.BorderWidth", 2)
        self.option_add("*Button.Relief", "ridge")

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
        self.playback_enabled = False
        self.playback_stream = None
        self.playback_buffer = deque()
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
            self.audio_interface.status_label.config(fg="#00ff00")

        if self.playback_enabled and self.playback_stream is None:
            self.start_playback_stream()




    def stop_stream(self):
        """ Stops the microphone audio stream """
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        if self.playback_stream is not None:
            self.playback_stream.stop()
            self.playback_stream.close()
            self.playback_stream = None

        self.audio_interface.status_label.config(text="Stream Stopped")
        self.audio_interface.status_label.config(fg="#ff0000")


    ####################################################################################################################################
    # Audio callback


    def audio_callback(self, indata, outdata, frames, time, status):
        """ Processes live audio input and applies modifications """
        processed_audio = self.modify_audio(indata)
        outdata[:, 0] = processed_audio.flatten()

        # store the processed audio in the buffer for a smooth playback
        if self.playback_enabled:
            if np.abs(indata).mean() > 0.05:
                self.playback_buffer.extend(processed_audio.flatten().tolist())
            else:
                self.playback_buffer.clear()

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
        if self.audio_interface.do_gain.get():
            gain_value = self.audio_interface.gain_slider.get()
            audio = loud_mic(audio, gain_value)

        # Downsample effect
        if self.audio_interface.do_downsample.get():
            audio = downsample(audio, self.audio_interface.downsample_slider.get(), 44100)

        # Apply bit depth reduction if enabled in the UI
        if self.audio_interface.do_bit_depth.get():
            bit_depth_value = self.audio_interface.bit_depth_slider.get()
            audio = reduce_bit_depth(audio, bit_depth_value)

        # Apply static noise if enabled in the UI and there's enough signal
        if self.audio_interface.do_static.get() and np.abs(audio).mean() > 0.01:
            # convert the slider value into a fractional intensity
            intensity = self.audio_interface.static_slider.get() / 100.0
            audio = add_static(audio, intensity=intensity)

        return audio


    ####################################################################################################################################
    # Separate stream for audio playback


    def start_playback_stream(self):
        """ Starts a separate non-blocking stream for real-time playback """
        if self.playback_stream is None:
            self.playback_stream = sd.OutputStream(
                samplerate=self.samplerate,
                channels=1,
                callback=self.playback_callback
            )
            self.playback_stream.start()




    def stop_playback_stream(self):
        """ Stops the playback stream """
        if self.playback_stream is not None:
            self.playback_stream.stop()
            self.playback_stream.close()
            self.playback_stream = None




    def playback_callback(self, outdata, frames, time, status):
        """Continuously plays the processed audio without blocking."""
        if len(self.playback_buffer) < frames:
            # Not enough data: output silence
            outdata.fill(0)
        else:
            # Pull 'frames' samples from the buffer
            for i in range(frames):
                outdata[i] = self.playback_buffer.popleft()


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

        if self.playback_enabled:
            self.start_playback_stream()
        else:
            self.stop_playback_stream()
