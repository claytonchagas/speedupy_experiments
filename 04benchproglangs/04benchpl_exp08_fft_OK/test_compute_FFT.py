#!/usr/bin/env python

#from __future__ import print_function

import numpy as np
import numpy.random as rn
import sys
import time

#import benchmark_decorator as dectimer
from intpy.intpy import initialize_intpy, deterministic

#@dectimer.bench_time(3)
@deterministic
def compute_FFT(n):
    """
        Compute the FFT of an n-by-n matrix of data
    """
    matrix = rn.rand(n, n) + 1j * rn.randn(n, n)
    result = np.fft.fft2(matrix)
    result = np.abs(result)

@initialize_intpy(__file__)
def main(n):
    compute_FFT(n)


if __name__=='__main__':
    n = int(sys.argv[1])
    
    dt1 = time.perf_counter()
    main(n)
    print(time.perf_counter() - dt1)