import numpy as np

def generate_complex_matrix(n):
    # Gere uma matriz n x n de números complexos aleatórios
    complex_matrix = np.random.rand(n, n) + 1j * np.random.rand(n, n)
    return complex_matrix

def save_complex_matrix_to_txt(matrix, filename):
    # Salve a matriz em um arquivo de texto no formato desejado
    with open(filename, 'w') as file:
        for row in matrix:
            row_str = ' '.join([f"{num.real}+{num.imag}i" for num in row])
            file.write(row_str + '\n')

if __name__ == '__main__':
    n = int(input("Digite o tamanho n da matriz: "))
    filename = input("Digite o nome do arquivo de saída: ")

    complex_matrix = generate_complex_matrix(n)
    save_complex_matrix_to_txt(complex_matrix, filename)

    print(f"Matriz {n}x{n} de números complexos gerada e salva em '{filename}'.")

