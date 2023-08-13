import time
import sys
from memoizer.DecoratorFactoryInstance import factory



@factory.decorator
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def main(n):
    print fib(n)


if __name__ == "__main__":
    n = int(sys.argv[1])
    start = time.time()
    main(n)
    print time.time()-start
