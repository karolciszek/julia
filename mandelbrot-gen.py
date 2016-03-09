#!/usr/bin/python
import numpy as np
import scipy.misc

ITERATION_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'
OUTPUT_FILE = 'out.png'
ITERS_PER_POINT = 200

# Interpolation functions: generate colour index
def linear(iteration):
    return float(iteration) / ITERS_PER_POINT
linear = np.vectorize(linear)

def smooth(iteration, escaped):
    log2 = np.log(2)
    mu = iteration + 1 - np.log(np.log(np.abs(escaped))) / log2
    index = mu / ITERS_PER_POINT if not np.isnan(mu) else 0
    return index
smooth = np.vectorize(smooth)

# Palette functions: generate RGB colour from index
def grayscale(index):
    colour = np.floor(255 * index)
    return (colour, colour, colour)
grayscale = np.vectorize(grayscale)

log2 = np.log(2)
def blueish(index):
    red_green = np.floor(102*np.log(index+1) / log2)
    blue = np.floor(161*np.log(index+1) / log2)
    return (red_green, red_green, blue)
blueish = np.vectorize(blueish)

if __name__ == '__main__':
    iterations = np.load(ITERATION_FILE)
    escaped_values = np.load(ESCAPED_FILE)

    width, height = iterations.shape
    # Scipy saves bitmaps in form (height, width, colour_channels)
    bitmap_dimensions = (height, width)

    def gen_channel(): return np.empty(bitmap_dimensions)
    red = gen_channel()
    green = gen_channel()
    blue = gen_channel()

    red, green, blue = blueish(smooth(iterations, escaped_values))

    # Changes the array to form bitmap[column][row][channel]
    # Transposing could be inefficient?
    bitmap = np.transpose([red, green, blue], (1, 2, 0))
    scipy.misc.imsave(OUTPUT_FILE, bitmap)
