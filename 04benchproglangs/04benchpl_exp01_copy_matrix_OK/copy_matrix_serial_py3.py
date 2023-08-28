#!/usr/bin/env python

import numpy as np
import sys
import time
from intpy import deterministic, initialize_intpy


def serial_copy(A,dimension):
    B = np.random.rand(dimension, dimension, 3)
    N = A.shape[0]
    for i in range(N):
        for j in range(N):
            B[i, j, 0] = A[i, j, 1]
            B[i, j, 2] = A[i, j, 0]
            B[i, j, 1] = A[i, j, 2]
    return B

if len(sys.argv) < 1:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' dimension')
    print('Please specify matrix dimensions')
    sys.exit()

def main():
    dimension = int(sys.argv[1])
    A = np.random.rand(dimension, dimension, 3)
    t0 = time.perf_counter()
    serial_copy(A,dimension)
    t1 = time.perf_counter()
    print(t1-t0)


if __name__ == '__main__':
    main()
