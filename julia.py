#!/usr/bin/python
import numpy as np
from numpy import log, isnan, isinf
import scipy.misc
import sys

ITER_NUM = 250
EPS = 0.01
BAILOUT = 2

xmin, xmax = (-0.1, 0.2)
ymin, ymax = (0.85j, 0.40j)
c = -0.8 + 0.156j
# c = -0.5 + 0.25j
# c = -0.123 + 0.745j
# Exponent in the Julia set
p = 2
# Number of 'trailing' elements when calculating Triangle Inequality Average
m = 7

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
def t(zpair):
    z_nminus1 = zpair[0] ** p
    z_n = zpair[1]
    mn = abs(abs(z_nminus1) - abs(c))
    Mn =  abs(z_nminus1) + abs(c)
    return (abs(z_n) - mn) / (Mn - mn)


# to be implemented later
def avg_sum(zs, i, m):
    if i - m == 0:
        return np.inf
    return sum(t(zs[n-2:n]) for n in range(m, i)) / (i - m)


def lin_inp(zs, d, i):
    last_iters_num = i if i < m else m
    return (d*avg_sum(zs, i, last_iters_num) +
            (1 - d)*avg_sum(zs[:-1], i, last_iters_num))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        m = int(sys.argv[1])

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
            print row

    scipy.misc.imsave('out.png', bitmap)
