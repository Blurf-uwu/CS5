# 1 & 2. Calculate base raised to exponent, default base = 10
def power(exponent, base=10):
    return base ** exponent

# 3. Sum all numbers in a list using arbitrary arguments (using arbitrary arguments)
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    return total


# 4. Print even numbers from a given list using arbitrary arguments (using arbitrary arguments)
def print_evens(*args):
    evens = [num for num in args if num % 2 == 0]
    if evens:
        print("Even numbers:", evens)
    else:
        print("No even numbers found.")
    return evens


# 5. Check whether a number is within a given range using arbitrary arguments (using arbitrary arguments)
def in_range(number, *args):
    if len(args) == 1:
        lower, upper = 0, args[0]
    elif len(args) == 2:
        lower, upper = args[0], args[1]
    else:
        return "Error: Provide 1 or 2 boundary values after the number."

    if lower <= number <= upper:
        return f"{number} is within the range [{lower}, {upper}]"
    else:
        return f"{number} is NOT within the range [{lower}, {upper}]"
    
print_evens(1,2,3,4,5,6,7,8,9,9,9,9,99,10,10)