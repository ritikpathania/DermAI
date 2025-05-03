Dict = {'Name': 'ABC', 1: [1, 2], '1': 'A'}
print(Dict)

print()
print(Dict['Name'])

print()
print(Dict.get(1))

print()
print(Dict.keys())

print()
print(Dict.values())

print()
print(Dict.items())

print()
Dict['2'] = 'B'
print(Dict)

print()
for i in Dict.items():
    print(i)

print()
for i in Dict:
    print(i)

print()
for i in Dict:
    print(Dict[i])

print()
for i, j in Dict.items():
    print(i, j)

print()
print(Dict.pop('2'))

print()
Dict.update({'1': 'C'})
print(Dict)

print()
print(Dict.popitem())

print()
print(Dict.clear())
