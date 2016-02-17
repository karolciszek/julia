import numpy as np
import scipy.misc

FILENAME = '3840.npy'
OUTPUT_FILE = 'out.png'
ITERS_PER_POINT = 200

def interpolate_color(iteration):
    linInp = np.floor(255 * (iteration / ITERS_PER_POINT))
    return [linInp, linInp, linInp]

mandelbrot_data = np.load(FILENAME)
(width, height) = mandelbrot_data.shape
bitmap = np.empty((width, height, 3))

for x in range(width):
    for y in range(height):
        color = interpolate_color(mandelbrot_data[x][y])
        bitmap[x][y] = color

scipy.misc.imsave(OUTPUT_FILE, bitmap)
