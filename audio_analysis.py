from typing import *
from scipy.fft import fft, fftfreq
import numpy as np


class AudioAnalyzer:
    def __init__(self, freq_mode, framerate):
        self.freq_mode = freq_mode
        self.framerate = framerate

    def estimate_freq(self, frames: Sequence):
        if self.freq_mode == "simple":
            return self.simple_estimate(frames)
        elif self.freq_mode == "fourier":
            return self.fourier_estimate(frames)

    def estimate_volume(self, frames: Sequence):
        return np.mean(frames)

    def simple_estimate(self, frames):
        raise Exception("Deprecated")

    def fourier_estimate(self, frames):
        num_frames = len(frames)
        freqs = fftfreq(num_frames, 1 / self.framerate)
        fft_signal = abs(fft(frames))
        dominant_frequency = freqs[np.argmax(fft_signal)]
        return abs(dominant_frequency)
