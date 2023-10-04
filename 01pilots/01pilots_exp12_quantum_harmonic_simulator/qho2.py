from __future__ import division
import numpy as np
import time, sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "speedupy"))

from intpy import initialize_intpy, deterministic

@deterministic
def coulomb_matrix(n):
    """
    Compute the Coulomb interaction matrix which has matrix elements

    C[j][k] = (psi_{2j+1},psi_{2k+1}/|x|) 

    Where psi is the normalized Hermite function
    """

    m = 2*n+1

    # Values of the Hermite functions at x=0
    psi0 = np.zeros(m)

    psi0[0] = np.pi**(-0.25)
    
    for k in range(1,m-1):
        psi0[k+1] = -np.sqrt(k/(k+1.0))*psi0[k-1]


    # The a-tilde coefficients of section 4
    A = np.eye(m)/2
    A[0,0] = 0.5
    A[0,1:] = psi0[:-1]/np.sqrt(2*np.sqrt(np.pi)*np.arange(1,m))
    A[1:,0] = A[0,1:]

    for j in range(1,m):
        for k in range(1,j):
            A[j,k] = psi0[j]*psi0[k-1]/np.sqrt(2*k) + np.sqrt(j/k)*A[j-1,k-1]
            A[k,j] = A[j,k]  

    # The b coefficients in section 4
    B = np.zeros((n,n)) 

    B[0,0] = 2/np.sqrt(np.pi)
    
    for k in range(1,n):
        B[0,k] = (4*A[1,2*k]-2*np.sqrt(k)*B[0,k-1])/np.sqrt(2*(2*k+1))
 
    B[1:,0] = B[0,1:]   
 
    for j in range(1,n):
        for k in range(1,n):
            B[j,k] = (4*A[2*j+1,2*k]-2*np.sqrt(k)*B[j,k-1])/ \
                     np.sqrt(2*(2*k+1))

    # Coulomb matrix
    C = np.zeros((n,n))
    for j in range(n):
        for k in range(n):
            if not (j+k) % 2:
                C[j,k] = B[j,k]   

    return C

@deterministic
def hermite_functions(x,n):
    """
    Evaluate the first n normalized Hermite functions on a grid x
    """

    m = len(x)
    psi = np.zeros((m,n))
    psi[:,0] = np.pi**(-0.25)*np.exp(-x**2/2)
    psi[:,1] = np.sqrt(2)*x*psi[:,0]
    a = np.sqrt(np.arange(0,n)/2)

    for k in range(1,n-1):
        psi[:,k+1] = (x*psi[:,k] - a[k]*psi[:,k-1])/a[k+1]

    return psi 

@initialize_intpy(__file__)
def main(x,n):
    t0 = time.perf_counter()
    hf = hermite_functions(x,2*n+1)
    t1 = time.perf_counter()    
    print(t1-t0)    

if __name__ == '__main__':
    length = int(sys.argv[1])
    n = int(sys.argv[2])
    x = np.linspace(-length,length,100)
    main(x,n)
    
    




  
