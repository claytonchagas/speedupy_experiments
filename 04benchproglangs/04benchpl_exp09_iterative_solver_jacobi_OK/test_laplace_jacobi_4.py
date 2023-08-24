# import numpy as np
# import sys

# import time

# from intpy import initialize_intpy, deterministic

# @deterministic
# def loop_time_step(u):
#     """
#         Take a time step in the desired numerical solution 
#         u found using loops
#     """
#     n, m = u.shape

#     error = 0.0
#     for i in range(1, n-1):
#         for j in range(1, m-1):
#             temp = u[i, j]
#             u[i, j] = (
#                        (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])*4.0 +
#                        u[i-1, j-1] + u[i-1, j+1] + u[i+1, j-1] +
#                        u[i+1, j+1]
#             )/20.0

#             difference = u[i, j] - temp
#             error += difference*difference

#     return u, np.sqrt(error)

# #----------------------
# # Function: loop_solver
# #----------------------

# @deterministic
# def loop_solver(n):
#     """
#         Find the desired numerical solution using loops
#     """

#     j = complex(0, 1)
#     pi_c = np.pi

#     # Set the initial condition
#     u = np.zeros((n, n), dtype=float)

#     #       Set the boundary condition
#     x = np.r_[0.0:pi_c:n*j]
#     u[0, :] = np.sin(x)
#     u[n-1, :] = np.sin(x)*np.exp(-pi_c)

#     iteration = 0
#     error = 2
#     while(iteration < 100000 and error > 1e-6):
#         (u, error) = loop_time_step(u)
#         iteration += 1
#     return (u, error, iteration)

# #---------------------------
# # Function: vector_time_step
# #---------------------------
# @deterministic
# def vector_time_step(u):
#     """
#         Take a time step in the desired numerical solution v 
#         found using vectorization
#     """
#     u_old = u.copy()
#     u[1:-1, 1:-1] = (
#                      (u[0:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, 0:-2] +
#                       u[1:-1, 2:])*4.0 +
#                      u[0:-2, 0:-2] + u[0:-2, 2:] + u[2:, 0:-2] + u[2:, 2:]
#     )/20.0

#     return u, np.linalg.norm(u-u_old)

# #----------------------------
# # Function: vectorized_solver
# #----------------------------
# @deterministic
# def vectorized_solver(n):
#     """
#         Find the desired numerical solution using vectorization
#     """
#     j = complex(0, 1)
#     pi_c = np.pi

#     # Set the initial condition
#     u = np.zeros((n, n), dtype=float)

#     # Set the boundary condition
#     x = np.r_[0.0:pi_c:n*j]
#     u[0, :] = np.sin(x)
#     u[n-1, :] = np.sin(x)*np.exp(-pi_c)

#     iteration = 0
#     error = 2
#     while(iteration < 100000 and error > 1e-6):
#         (u, error) = vector_time_step(u)
#         iteration += 1
#     return (u, error, iteration)


# # number of grid points
# @initialize_intpy(__file__)
# def main0(num_points):
#     (u, error, iteration) = loop_solver(num_points)

# # @initialize_intpy(__file__)    
# def main1(num_points):
#     (u, error, iteration) = vectorized_solver(num_points)
    

# if __name__ == '__main__':
#     num_points = int(sys.argv[1])
#     print('LOOP')
#     dti = time.perf_counter()
#     main0(num_points)
#     print(time.perf_counter() - dti)
#     print('VECTOR')
#     dti = time.perf_counter()
#     main1(num_points)
#     print(time.perf_counter() - dti)

import sys
from pathlib import Path
new_path = (Path('__file__').resolve().parent.parent.parent / "speedupy/").__str__()
sys.path.append(new_path)

import numpy as np

import time

from intpy import initialize_intpy, deterministic

@deterministic
def loop_time_step(u):
    """
        Take a time step in the desired numerical solution 
        u found using loops
    """
    n, m = u.shape

    error = 0.0
    for i in range(1, n-1):
        for j in range(1, m-1):
            temp = u[i, j]
            u[i, j] = (
                       (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])*4.0 +
                       u[i-1, j-1] + u[i-1, j+1] + u[i+1, j-1] +
                       u[i+1, j+1]
            )/20.0

            difference = u[i, j] - temp
            error += difference*difference

    return u, np.sqrt(error)

#----------------------
# Function: loop_solver
#----------------------

@deterministic
def loop_solver(n):
    """
        Find the desired numerical solution using loops
    """

    j = complex(0, 1)
    pi_c = np.pi

    # Set the initial condition
    u = np.zeros((n, n), dtype=float)

    #       Set the boundary condition
    x = np.r_[0.0:pi_c:n*j]
    u[0, :] = np.sin(x)
    u[n-1, :] = np.sin(x)*np.exp(-pi_c)

    iteration = 0
    error = 2
    while(iteration < 100000 and error > 1e-6):
        (u, error) = loop_time_step(u)
        iteration += 1
    return (u, error, iteration)

#---------------------------
# Function: vector_time_step
#---------------------------
@deterministic
def vector_time_step(u):
    """
        Take a time step in the desired numerical solution v 
        found using vectorization
    """
    u_old = u.copy()
    u[1:-1, 1:-1] = (
                     (u[0:-2, 1:-1] + u[2:, 1:-1] + u[1:-1, 0:-2] +
                      u[1:-1, 2:])*4.0 +
                     u[0:-2, 0:-2] + u[0:-2, 2:] + u[2:, 0:-2] + u[2:, 2:]
    )/20.0

    return u, np.linalg.norm(u-u_old)

#----------------------------
# Function: vectorized_solver
#----------------------------
@deterministic
def vectorized_solver(n):
    """
        Find the desired numerical solution using vectorization
    """
    j = complex(0, 1)
    pi_c = np.pi

    # Set the initial condition
    u = np.zeros((n, n), dtype=float)

    # Set the boundary condition
    x = np.r_[0.0:pi_c:n*j]
    u[0, :] = np.sin(x)
    u[n-1, :] = np.sin(x)*np.exp(-pi_c)

    iteration = 0
    error = 2
    while(iteration < 100000 and error > 1e-6):
        (u, error) = vector_time_step(u)
        iteration += 1
    return (u, error, iteration)


# number of grid points
# def main0(num_points):
    
# def main1(num_points):
    
@initialize_intpy(__file__)
def main():
    num_points = int(sys.argv[1])
    #print('LOOP')
    dti = time.perf_counter()
    #main0(num_points)
    (u, error, iteration) = loop_solver(num_points)
    print(time.perf_counter() - dti)
    #print('VECTOR')
    dti = time.perf_counter()
    #main1(num_points)
    (u, error, iteration) = vectorized_solver(num_points)
    print(time.perf_counter() - dti)

if __name__ == '__main__':
    main()
