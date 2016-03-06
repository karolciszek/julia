import numpy as np

iterations_per_point = 200
EPSILON = 0.01

ITER_FILE = 'iter.npy'
ESCAPED_FILE = 'escaped.npy'

x_min = -2.1
x_max = 0.7
width = 3840
y_min = 0
y_max = 0+1.2j
# preserving proportions in pixelheight
height = np.int(np.abs(y_max - y_min) * width / (x_max - x_min))

# numPy data type to store complex numbers
complex128bit = np.dtype('c16')
reals = np.linspace(x_min, x_max, width)
imags = np.linspace(y_min, y_max, height)

def iterations_to_escape(c):
    """Computes the Mandelbrot sequence for complex c"""
    z = 0
    #print("[{0}]".format(c))
    for i in range(iterations_per_point):
        z = z ** 2 + c
        if np.abs(z) >= 2: break
    return (i, z)

size = (width, height)
iterations = np.empty(size)
escaped_values = np.empty(size, complex128bit)

for x in range(width):
    if (x % 100 == 0): print x
    for y in range(height):
        (i, z) = iterations_to_escape(reals[x] + imags[y])
        iterations[x][y] = i
        escaped_values[x][y] = z

np.save(ITER_FILE, iterations)
np.save(ESCAPED_FILE, escaped_values)
