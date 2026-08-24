# (1) 14 in range(0, 2)
print(14 in range(0, 2))        # No

# (2) 14 in range(0, -2)
print(14 in range(0, -2))       # No

# (3) 14 in range(0, 100, 2)
print(14 in range(0, 100, 2))   # Yes

# (4) -14 in range(0, 100, -2)
print(-14 in range(0, 100, -2)) # No

# (5) 5 in range(5, -5, -5)
print(5 in range(5, -5, -5))    # Yes

# (6) 0 in range(5, -5, -5)
print(0 in range(5, -5, -5))    # Yes

# (7) -5 in range(5, -5, -5)
print(-5 in range(5, -5, -5))   # No

# (8) 70 in range(-111, 111, 3)
print(70 in range(-111, 111, 3))  # No

# (9) 71 in range(-111, 111, -3)
print(71 in range(-111, 111, -3)) # No

# (10) 72 in range(111, -111, -3)
print(72 in range(111, -111, -3)) # Yes
