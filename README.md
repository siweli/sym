# Shitify Your Mic

This program is designed to purposefully make your mic quality worse for comedic effect with friends.
Project started on 10/02/2025


## Requirements

Download and configure a virtual audio device, this is the one i use: https://vb-audio.com/Cable/

## Setup

Run the exe and press 'Output Devices', now look at the folder you ran the exe from and you'll see a 'devices.txt'. In that file is a list of your audio devices both input and output. Find your normal microphone device in the list (it will be there multiple times) and then find the virtual audio device that shares the same Host API as your input device. From my own testing I found the Host API 'MME' worked fine. You need to now open the config.cfg file in a normal text editor and replace the input_device number with the ID of your normal microphone device that you foudnin devices.txt, and the output_device with the ID of the virtual audio device. The wrong combination can result in some errors but some trial and error and youll find the correct device pair. Once found you won't have to change this unless you add new audio devices which may change the IDs around. Now you can re run the exe and it will automatically load your devices from the config.
