var = ('a', 'b', 'c', 'd', 'e')

print()
print(type(var))
print(len(var))
print(var[2])
print(var[-1])
print(var[0:])
print(var[0::2])
print(var[-3:-1])

print()
for i in var:
    print(i)

print()
for i in range(0, len(var)):
    print(var)
