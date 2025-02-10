import numpy as np
import scipy.signal


def loud_mic(audio, gain):
    """ Make the mic really loud """
    # increase gain
    audio *= gain

    # clip it to simulate clipping
    audio = np.clip(audio, -1, 1)
    return audio




def downsample(audio, downsample_rate, upsample_rate):
    """ Downscale to a poor quality then upscale it to reduce quality """
    # save original length
    original_length = len(audio)

    # resample the audio at the lower downsample rate then resample at the upsample rate
    audio = scipy.signal.resample(audio, int(original_length * downsample_rate / upsample_rate))
    audio = scipy.signal.resample(audio, original_length)
    return audio




def reduce_bit_depth(audio, bit_depth):
    """ Reduce bit depth """
    # Assuming audio is normalized between -1 and 1.
    levels = 2 ** bit_depth  # For 4 bits, that's 16 levels.

    # Normalize to [0, 1]
    audio_norm = (audio + 1) / 2
    # Quantize to a small number of levels
    audio_quantized = np.floor(audio_norm * levels) / levels
    # Convert back to [-1, 1]
    audio = audio_quantized * 2 - 1
    return audio