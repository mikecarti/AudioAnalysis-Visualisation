from typing import *
from scipy.fft import fft, fftfreq
import numpy as np

SQRT_TWO = 1.414


class AudioAnalyzer:
    def __init__(self, freq_mode, vol_mode, framerate):
        self.freq_mode = freq_mode
        self.vol_mode = vol_mode
        self.framerate = framerate

    def estimate_freq(self, frames: Sequence):
        if self.freq_mode == "simple":
            return self.simple_freq_estimate(frames)
        elif self.freq_mode == "fourier":
            return self.fourier_freq_estimate(frames)

    def simple_freq_estimate(self, frames):
        raise Exception("Deprecated")

    def fourier_freq_estimate(self, frames):
        num_frames = len(frames)
        freqs = fftfreq(num_frames, 1 / self.framerate)
        fft_signal = abs(fft(frames))
        # remove first frequencies to not get 0 frequency
        dominant_frequency = freqs[np.argmax(fft_signal[2:])]
        return abs(dominant_frequency)

    def estimate_volume(self, frames: Sequence):
        if self.vol_mode == 'simple':
            return self.simple_vol_estimate(frames)
        elif self.vol_mode == 'rms':
            return self.rms_vol_estimate(frames)

    def simple_vol_estimate(self, frames: Sequence):
        return np.mean(frames)

    def rms_vol_estimate(self, frames: Sequence):
        return np.sqrt(np.mean(np.square(frames))) * SQRT_TWO
