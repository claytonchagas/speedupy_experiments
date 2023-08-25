from intpy import initialize_intpy, deterministic
import time
import sys
import itertools

@deterministic
def chunks(l):
    """Divide a list of nodes `l` in `n` chunks"""
    n=int(len(l)/2)
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c, n))
        if not x:
            return
        return x
      
      
@initialize_intpy(__file__)
def main(l):
    print(chunks(l))
    
if __name__ == "__main__":
    l = (sys.argv[2:])
    l.pop()
    l.pop()
    for i in range(len(l)):
      l[i]=l[i][:-1]
    start = time.perf_counter()
    main(l)
    print(time.perf_counter()-start)
