import numpy as np
import matplotlib.pyplot as plt


def normalize(x):
    return 1 / (1 + np.exp(-x))


# class Colorizer:
def float_to_color(x: float) -> tuple:
    norm_x = normalize(x)
    return get_color(norm_x)


def get_color(normalized_x):
    jet_color = plt.cm.jet(normalized_x)[:3]
    return [255 * x for x in jet_color]
