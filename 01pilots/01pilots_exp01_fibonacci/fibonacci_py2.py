import sys
import time

def fib(n):
    return fib(n-1)+ fib(n-2) if n>1 else n

def main(n):
    t = time.time()
    fib(n)
    print time.time()-t

if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)
