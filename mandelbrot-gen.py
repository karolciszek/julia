#!/usr/bin/python
import numpy as np
import scipy.misc
from PIL import Image

ITERATION_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'
OUTPUT_FILE = 'out.png'
ITERS_PER_POINT = 200
log2 = np.log(2)


# Interpolation functions: generate colour index
def iteration_index(iteration):
    return float(iteration) / ITERS_PER_POINT
iteration_index = np.vectorize(iteration_index)


def smooth_index(iteration, escaped):
    mu = iteration + 1 - np.log(np.log(np.abs(escaped))) / log2
    index = mu / ITERS_PER_POINT if not (np.isnan(mu) or mu == ITERS_PER_POINT) else 0
    return index
smooth_index = np.vectorize(smooth_index)


# Palette functions: generate RGB colour from index
def greyscale(index):
    colour = np.floor(255 * index)
    return colour, colour, colour
greyscale = np.vectorize(greyscale)


def linear(index, end=(255, 255, 255), start=(0, 0, 0)):
    return tuple(np.floor(s + (e - s) * index) for s, e in zip(start, end))
linear = np.vectorize(linear)


def repeating(index, end=(255, 255, 255), start=(0, 0, 0), freq=3, phase=0):
    return tuple(np.floor(e + (e - s) * np.sin(index * freq + phase) / 2)
                 for s, e in zip(start, end))
repeating = np.vectorize(repeating)


def blueish(index):
    r_g = np.floor(102*np.log(index+1) / log2)
    b = np.floor(161*np.log(index+1) / log2)
    return r_g, r_g, b
blueish = np.vectorize(blueish)

if __name__ == '__main__':
    iterations = np.load(ITERATION_FILE)
    escaped_values = np.load(ESCAPED_FILE)

    width, height = iterations.shape
    # Scipy saves bitmaps in form (height, width, colour_channels)
    bitmap_dimensions = (height, width)

    def gen_channel(): return np.empty(bitmap_dimensions)
    # red = gen_channel()
    # green = gen_channel()
    # blue = gen_channel()

    r, g, b = repeating(smooth_index(iterations, escaped_values),
                        freq=8 * np.pi)
    print "Transposing"

    # Changes the array to form bitmap[column][row][c   hannel]
    # Transposing could be inefficient?
    bitmap = np.transpose([r, g, b], (1, 2, 0))
    scipy.misc.imsave(OUTPUT_FILE, bitmap)
