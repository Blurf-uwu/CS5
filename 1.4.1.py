# 1. Identify if a number is odd or even
def is_odd_or_even(number):
    if number % 2 == 0:
        return f"{number} is Even"
    else:
        return f"{number} is Odd"


# 2. Compute for the square of a number
def square(number):
    return number ** 2


# 3. Identify if a number is positive, negative, or zero
def check_sign(number):
    if number > 0:
        return f"{number} is Positive"
    elif number < 0:
        return f"{number} is Negative"
    else:
        return f"{number} is Zero"


# 4. Compute for the factorial of a number
def factorial(number):
    if number < 0:
        return "Factorial is not defined for negative numbers."
    elif number == 0 or number == 1:
        return 1
    else:
        result = 1
        for i in range(2, number + 1):
            result *= i
        return result


# 5. Identify if a number is divisible by another number
def is_divisible(number, divisor):
    if divisor == 0:
        return "Error: Cannot divide by zero."
    if number % divisor == 0:
        return f"{number} is divisible by {divisor}"
    else:
        return f"{number} is NOT divisible by {divisor}"


# 6. Identify the greatest number among three values
def greatest_of_three(a, b, c):
    greatest = max(a, b, c)
    return f"The greatest number among {a}, {b}, and {c} is: {greatest}"
