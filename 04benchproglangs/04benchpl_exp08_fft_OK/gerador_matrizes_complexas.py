import numpy as np
import sys

def generate_complex_matrix(n):
    complex_matrix = np.random.rand(n, n) + 1j * np.random.rand(n, n)
    return complex_matrix

def save_complex_matrix_to_txt(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            row_str = ' '.join([f"{num.real}+{num.imag}i" for num in row])
            file.write(row_str + '\n')

if __name__ == '__main__':
    n = int(sys.argv[1])
    filename = "fft_"+str(n)+".txt"
    complex_matrix = generate_complex_matrix(n)
    save_complex_matrix_to_txt(complex_matrix, filename)


