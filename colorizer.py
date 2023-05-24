import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal

MAX_FREQ = 22000
MAX_VOL = 800000000


def normalize_sigmoid(x):
    return 1 / (1 + np.exp(-x))


def normalize(x, min_x, max_x):
    return (x - min_x) / (max_x - min_x)


def frequency_to_color(freq: int, max_freq=MAX_FREQ):
    norm_x = normalize(freq, min_x=0, max_x=max_freq)
    return get_color(norm_x)


def volume_to_color(vol: int):
    norm_x = normalize(vol, min_x=0, max_x=MAX_VOL)
    return get_color(norm_x)


def get_color(normalized_x):
    jet_color = plt.cm.jet(normalized_x)[:3]
    return [255 * x for x in jet_color]
