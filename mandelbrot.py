#!/bin/python3
import numpy as np

iterations_per_point = 200
EPSILON = 0.01

ITER_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'

x_min, x_max = (-2.1, 0.7)
y_min, y_max = (-1.2j, 1.2j)

# width of resulting image in pixels
width = 40

# preserving proportions in pixelheight
y_range = np.abs(y_max - y_min)
x_range = x_max - x_min
height = np.int(y_range * width / x_range)

def iterations_to_escape(c):
    """Computes the Mandelbrot sequence for complex c"""
    z = 0
    for i in range(iterations_per_point):
        z = z ** 2 + c
        if np.abs(z) >= 2: break
    return (i, z)

# allows the function to be performed elementwise
iterations_to_escape = np.vectorize(iterations_to_escape)

# size = (width, height)
# iterations = np.empty(size)
# escaped_values = np.empty(size, complex128bit)

# numPy data type to store complex numbers
complex128bit = np.dtype('c16')
x_axis = np.linspace(x_min, x_max, width)
y_axis = np.linspace(y_min, y_max, height)

xs, ys = np.meshgrid(x_axis, y_axis)

(iterations, escaped_values) = iterations_to_escape(xs + ys)

# for x in range(width):
#     for y in range(height):
#         (i, z) = iterations_to_escape(reals[x] + imags[y])
#         iterations[x][y] = i
#         escaped_values[x][y] = z

np.save(ITER_FILE, iterations)
np.save(ESCAPED_FILE, escaped_values)
