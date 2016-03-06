import numpy as np
import scipy.misc

ITERATION_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'
OUTPUT_FILE = 'out.png'
ITERS_PER_POINT = 200

def linear_interpolation(iteration):
    linInp = np.floor(255 * (iteration / ITERS_PER_POINT))
    return [linInp, linInp, linInp]

def smooth_interpolation(iteration, escaped):
    log2 = np.log(2)
    mu = iteration + 1 - np.log(np.log(np.abs(escaped))) / log2
    col_base = np.floor(255 * mu / ITERS_PER_POINT) if (not np.isnan(mu)) else 0
    return [col_base, col_base, col_base]

iterations = np.load(ITERATION_FILE)
escaped_values = np.load(ESCAPED_FILE)

(width, half_height) = iterations.shape
# scipy saves bitmaps in form (height, width, colour_channels)
middleRowIndex = half_height - 1
bitmap_dimensions = (2 * half_height - 1, width, 3)
bitmap = np.empty(bitmap_dimensions)

for x in range(width):
    for y in range(half_height):
        color = smooth_interpolation(iterations[x][y], escaped_values[x][y])
        bitmap[middleRowIndex + y][x] = color
        bitmap[middleRowIndex - y][x] = color

scipy.misc.imsave(OUTPUT_FILE, bitmap)
