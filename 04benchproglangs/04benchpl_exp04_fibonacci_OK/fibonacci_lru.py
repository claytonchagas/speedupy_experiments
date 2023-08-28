#!/usr/bin/env python

import sys
import time

from functools import lru_cache

@lru_cache(maxsize=100)
def iterative_fibonacci(n):
    if n < 2:
        return n
    previous_fibonacci = 1
    current_fibonacci = 1
    for num in range(2, n):
        previous_fibonacci, current_fibonacci = current_fibonacci, \
            current_fibonacci + previous_fibonacci
    return current_fibonacci


@lru_cache(maxsize=100)
def recursive_fibonacci(n):
    if n < 2:
        return n
    else:
        return recursive_fibonacci(n-1) + recursive_fibonacci(n-2)


if len(sys.argv) < 1:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' N')
    print('Please specify the number of iterations.')
    sys.exit()


def main():
    N = int(sys.argv[1])
    t0 = time.perf_counter()
    n1 = iterative_fibonacci(N)
    t1 = time.perf_counter()
    n2 = recursive_fibonacci(N)
    t2 = time.perf_counter()
    print(t1-t0)
    print(t2-t1)

if __name__ == '__main__':
    main()
