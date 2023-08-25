import numpy as np
from itertools import combinations
from collections import Counter
import time

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from intpy import initialize_intpy, deterministic

np.random.seed(0)

def repeat_mutation_sim(G, N, L, mu=3e-8):
    """
    Generate N repeats of length L mutating at rate
    mu for G generations.
    """
    repeat_alleles = list()
    for i in range(N):
        num_mutations = np.random.poisson(L*mu*G)
        positions = np.random.choice(list(range(L)), size=num_mutations, replace=False)
        repeat_alleles.append(positions)
    return repeat_alleles

@deterministic 
def count_shared_mutations(sims):
    counts = Counter()
    i = 0
    for p1, p2 in combinations(sims, 2):
        # if i % 10000000 == 0:
        #     print("\ttotal pairs counted: %d\n" % i, end=' ')
        # i += 1
        num_shared = len(set(p1).intersection(set(p2)))
        counts[num_shared] += num_shared
    return counts

@initialize_intpy(__file__)
def main(n):
    return count_shared_mutations(n)
 
if __name__ == "__main__":
    x = repeat_mutation_sim(1e6, 12162, 156)
    t1 = time.perf_counter()
    shared_counts = main(x)
    print(time.perf_counter()-t1)

