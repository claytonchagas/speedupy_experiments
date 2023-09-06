#!/usr/bin/env python

#from __future__ import print_function

import numpy as np
import numpy.random as rn
import sys
import time

#import benchmark_decorator as dectimer
from intpy import initialize_intpy, deterministic

#@dectimer.bench_time(3)

def load_matrix(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            row = [complex(x.replace('i', 'j')) for x in line.split()]
            matrix.append(row)
        return np.array(matrix)


@deterministic
def compute_FFT(A):
    result = np.fft.fft2(A)
    result = np.abs(result)
    return result

@initialize_intpy(__file__)
def main(filename):
    A=load_matrix(filename)
    # print(A)
    compute_FFT(A)


if __name__=='__main__':
    filename = sys.argv[1]
    dt1 = time.perf_counter()
    main(filename)
    print(time.perf_counter() - dt1)
