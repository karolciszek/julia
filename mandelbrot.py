import numpy as np
#import matplotlib as mpl
#import scipy.misc

iterationsPerPoint = 200
EPSILON = 0.01

xMin = -2.1
xMax = 0.7
xHeight = 3840
yMin = 0-1.2j
yMax = 0+1.2j
# preserving proportions in pixelheight
yHeight = np.int(np.abs(yMax - yMin) * xHeight / (xMax - xMin))

# numPy data type to store complex numbers
complex128bit = np.dtype('c16')
reals = np.linspace(xMin, xMax, xHeight)
imags = np.linspace(yMin, yMax, yHeight)

def iterationsToEscape(c):
    """Computes the Mandelbrot sequence for complex c"""
    z = 0
    #print("[{0}]".format(c))
    for i in range(iterationsPerPoint):
        z = z ** 2 + c
        if np.abs(z) >= 2: return i
    return 0

def interpolateColor(iteration):
    linInp = np.floor(255 * (iteration / iterationsPerPoint))
    return [linInp, linInp, linInp]


# colour represented as int value between 0 and 255
# there is a bitmap for each colour channel
# bitmap = np.empty((yHeight, xHeight, 3))

for y in range(yHeight):
    for x in range(xHeight):
        iteration = iterationsToEscape(reals[x] + imags[y])
        print("({0},{1}),{2},[{3},{4}]".format(x, y, iteration, reals[x], imags[y]))
        # colour = interpolateColor(iteration)
        # bitmap[y][x] = colour

# scipy.misc.imsave("out.png", bitmap)
