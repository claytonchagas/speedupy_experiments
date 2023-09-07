
from intpy import initialize_intpy, deterministic

import time

@deterministic
def raised_to_string(x):
    """
        Convert to int, then raise the input to the power of itself.
    """
    x = int(x)
    if x == 0:
        return 0
    else:
        return x**x

@deterministic
def raised_to(x):
    """
        Raise the input to the power of itself
    """
    if x == 0:
        return 0
    else:
        return x**x

@deterministic # mesmo usando essa variável global, achei o caso colocar @deterministc
def is_munchausen_number(i,power_of_digits):
    return i == sum(power_of_digits[int(x)] for x in str(i))


def find_munchausen_numbers():
    """
        Find the 4 Munchausen numbers
    """
    power_of_digits = [raised_to(i) for i in range(10)]
    number = 0
    i = 0
    while True:
        if is_munchausen_number(i,power_of_digits):
            number += 1
            print("Munchausen number %d: %d" % (number, i))

        if (number == 4):
            break

        i += 1

# def find_munchausen_numbers_map():
#     """
#         Find the 4 Munchausen numbers using map()
#     """
#     num = 0
#     i = 0
#     while True:
#         if i == sum(map(raised_to_string, str(i))):
#             num += 1
#             print("Munchausen number %d: %d" %(num, i))
#         if (num == 4):
#             break
#         i += 1

@initialize_intpy(__file__)
def main():
    find_munchausen_numbers()

if __name__ == '__main__':
    dti = time.perf_counter()
    main()
    print(time.perf_counter() - dti)
