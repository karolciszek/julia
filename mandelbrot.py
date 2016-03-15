#!/usr/bin/python2
import numpy as np
from numpy import abs

iterations_per_point = 200
EPSILON = 0.01
power = 2

DATA_FILE = 'itertest.npy'
# ESCAPED_FILE = 'escaped_mi.npy'

x_min, x_max = (-2.1, 0.7)
y_min, y_max = (-1.2j, 1.2j)

# Width of resulting image in pixels
width = 150

# Preserving proportions in pixel-height
y_range = np.abs(y_max - y_min)
x_range = x_max - x_min
height = np.int(y_range * width / x_range)


def iterations_to_escape(c):
    """Computes the Mandelbrot sequence for complex c"""
    zs = np.empty(iterations_per_point, dtype='complex64')
    z = 0
    if c == 0 and power < 0:
        zs[0] = c
        return 0, zs
    for i in range(iterations_per_point):
        z = np.power(z, power) + c
        zs[i] = z
        if abs(z) >= 2: break
    return c, i, z

# Allows the function to be performed element-wise
iterations_to_escape = np.vectorize(iterations_to_escape)

if __name__ == '__main__':
    x_axis = np.linspace(x_min, x_max, width)
    y_axis = np.linspace(y_min, y_max, height)
    xs, ys = np.meshgrid(x_axis, y_axis)

    data_type = 'complex64, int, {}complex64'.format(iterations_per_point)
    output_data = np.empty((height, width), dtype=data_type)

    for col in range(height):
        for row in range(width):
            output_data[col][row] = iterations_to_escape(x_axis[row] + y_axis[col])

    # Data saved in triples (complex_param, num_of_iters, iterated_values)
    np.save(DATA_FILE, output_data)
