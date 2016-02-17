import numpy as np
import re as regex
import scipy.misc

WIDTH = 3840
HEIGHT = 3291
PRINT_FREQUENCY = 100000

f = open('3840.out', 'r')

output_np_array = np.empty((WIDTH, HEIGHT))

pattern = regex.compile('[0-9\.\-]+')
n = 0
for line in f:
    # Encoding-specific parsing. Bit dirty.
    # Encoding in file:
    # (x-pixel,y-pixel),iterations,[real-component,imag-component]
    tokens = regex.findall(pattern, line)

    iterations = int(tokens[2])
    xPos = int(tokens[0])
    yPos = int(tokens[1])
    output_np_array[xPos][yPos] = iterations

    n += 1
    if (n % 100000 == 0): print n

np.save('3840.npy', output_np_array)
# scipy.misc.imsave("out.png", bitmap)
