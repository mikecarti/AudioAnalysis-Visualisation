import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal

MAX_FREQ = 22000
MAX_VOL = 800000000


def normalize_frequency(freq: int, max_x=MAX_FREQ):
    return normalize(freq, min_x=0, max_x=max_x)


def normalize_volume(volume: float, max_x=MAX_VOL):
    return normalize(volume, min_x=0, max_x=max_x)


def normalize(x, min_x=0, max_x=10 ** 10):
    return (x - min_x) / (max_x - min_x)


def get_color(normalized_x):
    jet_color = plt.cm.jet(normalized_x)[:3]
    return [255 * (1 - x) for x in jet_color]
