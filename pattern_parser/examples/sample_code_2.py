def factorial(n):
    """Recursive factorial function."""
    if n == 0:
        return 1
    return n * factorial(n - 1)

def is_even(num):
    return num % 2 == 0

def print_list(items):
    for item in items:
        print(item)

def dummy():
    pass
