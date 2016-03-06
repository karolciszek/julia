#!/bin/python3
import numpy as np
import scipy.misc

ITERATION_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'
OUTPUT_FILE = 'out.png'
ITERS_PER_POINT = 200

def linear_interpolation(iteration):
    linInp = np.floor(255 * (iteration / ITERS_PER_POINT))
    return [linInp, linInp, linInp]
linear_interpolation = np.vectorize(linear_interpolation)

def smooth_interpolation(iteration, escaped):
    log2 = np.log(2)
    mu = iteration + 1 - np.log(np.log(np.abs(escaped))) / log2
    col_base = np.floor(255 * mu / ITERS_PER_POINT) if (not np.isnan(mu)) else 0
    return col_base
smooth_interpolation = np.vectorize(smooth_interpolation)

iterations = np.load(ITERATION_FILE)
escaped_values = np.load(ESCAPED_FILE)

(width, height) = iterations.shape
# scipy saves bitmaps in form (height, width, colour_channels)
bitmap_dimensions = (height, width, 3)
bitmap = np.empty(bitmap_dimensions)

bitmap = smooth_interpolation(iterations, escaped_values)
print(bitmap)

scipy.misc.imsave(OUTPUT_FILE, bitmap)
