# Arithmetic Operators
a = 9
b = 4

Add = a + b
Sub = a - b
Mul = a * b
floatDiv = a / b
floorDiv = a // b
Mod = a % b
P = a ** b

print()
print(Add)
print(Sub)
print(Mul)
print(floatDiv)
print(floorDiv)
print(Mod)
print(P)

# Comparison Operators
a = 9
b = 4

print()
print(a > b)
print(a < b)
print(a == b)
print(a != b)
print(a >= b)
print(a <= b)

# Logical Operators
a = True
b = False

print()
print(a and b)
print(a or b)
print(not a)

# Bitwise operators
a = 9
b = 4

print()
print(a & b)
print(a | b)
print(~a)
print(a ^ b)
print(a >> 2)
print(a << 2)

# Assignment Operators
a = 10

print()
b = a
print(b)

b += a
print(b)

b -= a
print(b)

b *= a
print(b)

b <<= a
print(b)

# Identity Operators
a = 10
b = 20
c = a

print()
print(a is not b)
print(a is c)

# Membership Operators
a = 24
b = 20

myList = [10, 20, 30, 40, 50]

if a not in myList:
    print("\nx is NOT present in given list")
else:
    print("\nx is present in given list")

if b in myList:
    print("y is present in given list")
else:
    print("y is NOT present in given list")
