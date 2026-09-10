def inforloop(a, b, c, d=1):
    numbers = range(b,c,d)
    for number in numbers:
        print(number)
    print(a in numbers)
    print(" ")


# (1) 14 in range(0, 2)
inforloop(14, 0, 2)

# (2) 14 in range(0, -2)
inforloop(14, 0, -2)

# (3) 14 in range(0, 100, 2)
inforloop(14, 0, 100, 2)

# (4) -14 in range(0, 100, -2)
inforloop(-14, 0, 100, -2)

# (5) 5 in range(5, -5, -5)
inforloop(5, 5, -5, -5)

# (6) 0 in range(5, -5, -5)
inforloop(0, 5, -5, -5)

# (7) -5 in range(5, -5, -5)
inforloop(-5, 5, -5, -5)

# (8) 70 in range(-111, 111, 3)
inforloop(70, -111, 111, 3)

# (9) 71 in range(-111, 111, -3)
inforloop(71, -111, 111, -3)

# (10) 72 in range(111, -111, -3)
inforloop(72, 111, -111, -3)
