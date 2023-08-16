from intpy import initialize_intpy, deterministic
import time
import sys
import numpy as np


@deterministic
def median(vals):
    count = len(vals)
    if count == 1:
        return float(vals[0])
    vals = sorted(vals)
    idx1 = int(count/2)
    idx2 = idx1 + 1
    #are we odd?
    if float(idx1) != count/2.0:
        idx1 = idx2
    return int(vals[idx1]+vals[idx2])/2.0 
    
   
 

@initialize_intpy(__file__)
def main(vals):
    print(median(vals))
  

if __name__ == "__main__":
    vals = (sys.argv[2:])
    vals.pop()
    vals.pop()
    for i in range(len(vals)):
      vals[i]=vals[i][:-1]
    start = time.perf_counter()
    main(vals)
    print(time.perf_counter()-start)
