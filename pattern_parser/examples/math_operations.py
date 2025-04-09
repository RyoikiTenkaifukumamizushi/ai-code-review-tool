def add(a, b):
    return a + b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Division by zero is not allowed."