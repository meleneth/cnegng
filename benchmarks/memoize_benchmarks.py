import timeit
from functools import lru_cache

# Custom memoize_method using try/except
def memoize_method(attr_name):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            try:
                return getattr(self, attr_name)
            except AttributeError:
                result = method(self, *args, **kwargs)
                setattr(self, attr_name, result)
                return result
        return wrapper
    return decorator

# Class using custom memoization
class SomeClassCustomMemo:
    @memoize_method('_some_foo')
    def some_foo(self):
        return 42

# Class using functools.lru_cache
class SomeClassLRUCache:
    @lru_cache(maxsize=None)
    def some_foo(self):
        return 42

# Benchmarking function for both approaches
def benchmark():
    # Instantiate both classes
    custom_memo_obj = SomeClassCustomMemo()
    lru_cache_obj = SomeClassLRUCache()

    # Time the custom memoization method
    custom_memo_time = timeit.timeit(lambda: custom_memo_obj.some_foo(), globals=globals(), number=1000000)

    # Time the lru_cache method
    lru_cache_time = timeit.timeit(lambda: lru_cache_obj.some_foo(), globals=globals(), number=1000000)

    # Print results
    print(f"Custom memoization time: {custom_memo_time:.6f} seconds")
    print(f"lru_cache memoization time: {lru_cache_time:.6f} seconds")

if __name__ == '__main__':
    benchmark()
