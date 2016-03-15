#!/usr/bin/python
import numpy as np
from numpy import isnan, isinf
import scipy.misc
import sys
from julia import t, avg_sum, lin_inp

ITERATION_FILE = 'itertest.npy'
ESCAPED_FILE = 'escaped_minus1.npy'
OUTPUT_FILE = 'img_edit/mandelbrot_-1/out.png'
ITERS_PER_POINT = 200
log2 = np.log(2)


# Interpolation functions: generate colour index
def iteration_index(iteration):
    return float(iteration) / ITERS_PER_POINT
iteration_index = np.vectorize(iteration_index)


def smooth_index(iteration, escaped):
    mu = iteration + 1 - np.log(np.log(np.abs(escaped))) / log2
    if not np.isnan(mu) and not mu == ITERS_PER_POINT:
        return mu / ITERS_PER_POINT
    else:
        return 0
smooth_index = np.vectorize(smooth_index)

# Palette functions: generate RGB colour from index
def greyscale(index):
    colour = np.floor(255 * index)
    return colour, colour, colour

if __name__ == '__main__':
    if len(sys.argv) == 2:
        num_avg_elems = int(sys.argv[1])
    else:
        num_avg_elems = 10
    path = 'img_edit/mandelbrot_-1/m' + str(num_avg_elems) + '.png'

    file_data = np.load(ITERATION_FILE)
    print np.shape(file_data)
    print file_data.dtype
    (argand_points, iterations, zs_arrays) = file_data

    width, height = iterations.shape
    # Scipy saves bitmaps in form (height, width, colour_channels)
    bitmap = np.empty(height, width)


    for row in range(width):
        for col in range(height):
            point = argand_points[width][height]
            numiters = iterations[width][height]
            iterated_zs = zs_arrays[width][height]

            smooth_count = smooth_index(iterated_zs[numiters - 1], numiters)

            index = lin_inp(iterated_zs, smooth_count % 1.0,
                            numiters, num_avg_elems, point)

            if isnan(index) or isinf(index):
                index = 0

            bitmap[col][row] = index
    scipy.misc.imsave(OUTPUT_FILE, bitmap)
