D = dict()
print(D)
n = int(input("\nEnter the no. of keys: "))
for i in range(1, n + 1):
    key = input("\nEnter key: ")
    value = input("Enter value: ")
    D[key] = [value]
print()
print(D)
