import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

import time

def find_gc(seq):
    """ Calculate GC content """

    if not seq:
        return 0

    gc = len([base for base in seq.upper() if base in 'CG'])
    return (gc * 100) / len(seq)
    

def main(seq):
    find_gc(seq)
  

if __name__ == "__main__":
    texto = ''
    with open(sys.argv[1]) as f:
        texto = "".join(f.readlines())
    start = time.time()
    main(texto)
    print(time.time()-start)
