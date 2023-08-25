#!/usr/bin/env python

import numpy as np
import sys

import time

from intpy import initialize_intpy, deterministic

#--------------------------------
# Function: matrix_multiplication
#--------------------------------

@deterministic
def matrix_multiplication(A, B):
    """
        Evaluate the dot product of matrices A and B using numpy
    """
    return np.dot(A, B)
    

@initialize_intpy(__file__)
def main(A,B):
    print(matrix_multiplication(A, B))

if __name__ == '__main__':
    N = int(sys.argv[1])
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)
    dti = time.perf_counter()
    main(A,B)
    print(time.perf_counter() - dti)
