import time

import numpy as np

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from intpy import initialize_intpy, deterministic


@deterministic
def get_empirical_CVaR(rewards, alpha = 0.9):
    
    a = sorted(list(rewards).copy(), reverse= True)

    for i in range(len(a)):
      a[i] = int(a[i])

    a = np.array(a)

    p = 1. * (np.arange(len(a)) + 1) / len(a)
    q_a = a[np.where(p >= (1 - alpha) )[0][0]]

    check = a < q_a

    if (np.where(check == True)[0]).size == 0:
        ind = 0
        temp = a[:ind + 1]
    else:
        ind = (np.where(check == True)[0][0] - 1)
        temp = a[:ind + 1]

    return (sum(temp) / len(temp))  
    
   
 

@initialize_intpy(__file__)
def main(rewards):
    print(get_empirical_CVaR(rewards, 0.9))
  

if __name__ == "__main__":
    n = [int(x) for x in sys.argv[1:-2]]
    start = time.perf_counter()
    main(n)
    print(time.perf_counter()-start)
