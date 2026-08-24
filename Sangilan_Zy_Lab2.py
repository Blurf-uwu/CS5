# (1) 14 in range(0, 2)
for i in range(0, 2):
    print(i)
print(14 in range(0, 2))        # No
print(" ")

# (2) 14 in range(0, -2)
for i in range(0, -2):
    print(i)
print(14 in range(0, -2))       # No
print(" ")

# (3) 14 in range(0, 100, 2)
for i in range(0, 100, 2):
    print(i)
print(14 in range(0, 100, 2))   # Yes
print(" ")

# (4) -14 in range(0, 100, -2)
for i in range(0, 100, -2):
    print(i)
print(-14 in range(0, 100, -2)) # No
print(" ")

# (5) 5 in range(5, -5, -5)
for i in range(5, -5, -5):
    print(i)
print(5 in range(5, -5, -5))    # Yes
print(" ")

# (6) 0 in range(5, -5, -5)
for i in range(5, -5, -5):
    print(i)
print(0 in range(5, -5, -5))    # Yes
print(" ")

# (7) -5 in range(5, -5, -5)
for i in range(5, -5, -5):
    print(i)
print(-5 in range(5, -5, -5))   # No
print(" ")

# (8) 70 in range(-111, 111, 3)
for i in range(-111, 111, 3):
    print(i)
print(70 in range(-111, 111, 3))  # No
print(" ")

# (9) 71 in range(-111, 111, -3)
for i in range(-111, 111, -3):
    print(i)
print(71 in range(-111, 111, -3)) # No
print(" ")

# (10) 72 in range(111, -111, -3)
for i in range(111, -111, -3):
    print(i)
print(72 in range(111, -111, -3)) # Yes
print(" ")
