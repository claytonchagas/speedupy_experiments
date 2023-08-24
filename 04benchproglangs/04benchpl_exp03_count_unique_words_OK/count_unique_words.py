#!/usr/bin/env python

from collections import defaultdict
import sys
import time
from intpy import deterministic, initialize_intpy

punctuation_characters = "~`!@#$%^&*()_-+=[{]}\|;:',<.>/?1234567890"

@deterministic
def strip_word(word):
    return "".join([x for x in word if x not in
                    punctuation_characters]).strip('\"').lower()

@deterministic
def count_words_dictionary(file_name):
    dictionary = defaultdict(int)
    for word in open(file_name).read().split():
        dictionary[strip_word(word)] += 1
    try:
        del dictionary['']
    except KeyError:
        pass
    return len(dictionary)

@deterministic 
def count_words_set(file_name):
    with open(file_name, "r") as file_id:
        lines = file_id.read().splitlines()
        uniques = set()
        for line in lines:
            uniques |= set(strip_word(m) for m in line.split())
    try:
        uniques.remove('')
    except KeyError:
        pass
    return len(uniques)


if len(sys.argv) < 1:
    print('Usage:')
    print('     python ' + sys.argv[0] + ' file_name')
    print('Please specify the file name')
    sys.exit()

@initialize_intpy(__file__)
def main():
    file_name = sys.argv[1]
    t0 = time.perf_counter()
    n = count_words_dictionary(file_name)
    t1 = time.perf_counter()
    n = count_words_set(file_name)
    t2 = time.perf_counter()
    print(t1-t0)
    print(t2-t1)

if __name__ == "__main__":
    main()
