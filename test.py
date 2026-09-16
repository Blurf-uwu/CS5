import sympy as smp
x, y = smp.symbols("x y")
b = smp.diff(x**2,x)
print(b)
