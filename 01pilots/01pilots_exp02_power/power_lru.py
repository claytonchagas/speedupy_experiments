import time
import sys
from functools import lru_cache

@lru_cache(maxsize=100)
def pow(n, m):
    if m == 0:
        return 1
    return n*pow(n, m-1)


def main(n, m):
    print(pow(n, m))


if __name__ == "__main__":
    n, m = int(sys.argv[1]), int(sys.argv[2])
    start = time.perf_counter()
    main(n, m)
    print(time.perf_counter()-start)
