from intpy import initialize_intpy, deterministic
import time
import sys


@deterministic
def find_gc(seq: str) -> float:
    """ Calculate GC content """

    if not seq:
        return 0

    gc = len([base for base in seq.upper() if base in 'CG'])
    return (gc * 100) / len(seq)
    
    
   
 

@initialize_intpy(__file__)
def main(seq):
    print(find_gc(seq))
  

if __name__ == "__main__":
    texto = ''
    with open(sys.argv[1]) as f:
        texto = "".join(f.readlines())
    start = time.perf_counter()
    main(texto)
    print(time.perf_counter()-start)
