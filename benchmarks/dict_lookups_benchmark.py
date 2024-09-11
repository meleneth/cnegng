#!/usr/bin/env python

import timeit

# Dummy function that does nothing
def some_func(value):
    pass

# The dictionary we will look up values from
some_dict = {
    'a': 1,
    'b': 2,
    'c': 3
}

# Method 1: Using 'in' check and lookup
def lookup_with_in(some_key):
    if some_key in some_dict:
        some_func(some_dict[some_key])

# Method 2: Using walrus operator
def lookup_with_walrus(some_key):
    if (value := some_dict.get(some_key)) is not None:
        some_func(value)

# Method 3: Using try-except to catch KeyError

def lookup_with_try_except(some_key):
    try:
        some_func(some_dict[some_key])
    except KeyError:
        pass

# Benchmarking

def benchmark():
    keys_to_test = ['a', 'd']  # 'a' exists, 'd' does not exist
    
    number_of_iterations = 1000000

    # Benchmarking the 'in' check method
    time_in_success = timeit.timeit("lookup_with_in('a')", globals=globals(), number=number_of_iterations)
    time_in_fail = timeit.timeit("lookup_with_in('d')", globals=globals(), number=number_of_iterations)

    # Benchmarking the walrus operator method
    time_walrus_success = timeit.timeit("lookup_with_walrus('a')", globals=globals(), number=number_of_iterations)
    time_walrus_fail = timeit.timeit("lookup_with_walrus('d')", globals=globals(), number=number_of_iterations)

    # Benchmarking the try-except method
    time_try_except_success = timeit.timeit("lookup_with_try_except('a')", globals=globals(), number=number_of_iterations)
    time_try_except_fail = timeit.timeit("lookup_with_try_except('d')", globals=globals(), number=number_of_iterations)


    # Print results

    print(f"In-check method (success): {time_in_success:.6f} seconds")
    print(f"In-check method (fail): {time_in_fail:.6f} seconds")
    print(f"Walrus operator method (success): {time_walrus_success:.6f} seconds")
    print(f"Walrus operator method (fail): {time_walrus_fail:.6f} seconds")
    print(f"Try-except method (success): {time_try_except_success:.6f} seconds")
    print(f"Try-except method (fail): {time_try_except_fail:.6f} seconds")

# Running the benchmark
if __name__ == "__main__":
    benchmark()

