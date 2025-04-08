def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def multiply(x, y):
    result = x * y
    return result

class Calculator:
    def divide(self, a, b):
        """Divides a by b."""
        if b == 0:
            return None
        return a / b

    def greet_user(self, name):
        print("Hello", name)
