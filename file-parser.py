import numpy as np
import re as regex
import scipy.misc

f = open('3840.out', 'r')

iterationsPerPoint = 200
def interpolateColor(iteration):
    linInp = np.floor(255 * (iteration / iterationsPerPoint))
    return [linInp, linInp, linInp]

bitmap = np.empty((3840, 3291, 3))

n = 0
for line in f:
    # Encoding-specific parsing. Bit dirty.
    # Encoding in file:
    # (x-pixel,y-pixel),iterations,[real-component,imag-component]
    pattern = regex.compile('[0-9\.\-]+')
    tokens = regex.findall(pattern, line)

    iterations = int(tokens[2])
    xPos = int(tokens[0])
    yPos = int(tokens[1])

    clr = interpolateColor(iterations)
    bitmap[xPos][yPos] = clr
    n += 1
    print(n)

scipy.misc.imsave("out.png", bitmap)
