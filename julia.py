#!/usr/bin/python
import numpy as np
from numpy import log, isnan, isinf
import scipy.misc
import sys
# for performance analysis
# import cProfile

ITER_NUM = 250
EPS = 0.01
BAILOUT = 2

xmin, xmax = (-1.5, 1.5)
ymin, ymax = (-1.0j, 1.0j)
c = -0.4 + 0.65j
abs_c = abs(c)
# c = -0.5 + 0.25j
# c = -0.123 + 0.745j
# Exponent in the Julia set
p = 2
# Number of 'trailing' elements when calculating Triangle Inequality Average
m = 10

width = 150
yrange = np.abs(ymax - ymin)
xrange = xmax - xmin
height = np.int(yrange * width / xrange)


def julia(z):
    zs = np.empty(ITER_NUM, dtype='complex64')
    for i in range(ITER_NUM):
        z = z ** 2 + c
        zs[i] = z
        if abs(z) >= BAILOUT: return i, zs
    return ITER_NUM, zs


# Functions for "Smooth Iteration Count"
def smooth_iter(z, iters):
    # return iters + 1 - log(log(abs(z))) / log(m)
    return iters + 1 + log(log(BAILOUT) / log(abs(z))) / log(p)


# Functions for Triangle Inequality Average method for colouring fractals
# Pre: zs has at least two elements
def t(zn_minus1, zn):
    abs_zn_minus1 = abs(zn_minus1 ** p)

    mn = abs(abs_zn_minus1 - abs_c)
    Mn = abs_zn_minus1 + abs_c
    return (abs(zn) - mn) / (Mn - mn)


# to be implemented later
def avg_sum(zs, i, m):
    if i - m == 0:
        return np.inf
    return sum(t(zs[n - 2], zs[n - 1]) for n in range(m, i)) / (i - m)


def lin_inp(zs, d, i):
    last_iters_num = i if i < m else m
    return (d*avg_sum(zs, i, last_iters_num) +
            (1 - d)*avg_sum(zs[:-1], i, last_iters_num))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        m = int(sys.argv[1])
    path = 'm' + str(m) + '.png'

    xaxis = np.linspace(xmin, xmax, width)
    yaxis = np.linspace(ymin, ymax, height)

    bitmap = np.zeros((height, width))

    for row in range(width):
        for col in range(height):
            z = xaxis[row] + yaxis[col]
            iters, zs = julia(z)
            smooth = smooth_iter(zs[iters - 1], iters)

            index = lin_inp(zs, smooth % 1.0, iters)
            if isnan(index) or isinf(index):
                index = 0

            bitmap[col][row] = index
        if row % 10 == 0:
            pass
            #print row
    scipy.misc.imsave(path, bitmap)

# if __name__ == '__main__':
    # cProfile.run('main()')
