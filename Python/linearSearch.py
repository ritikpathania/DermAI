def linear_search(lst, key):
    for i in range(len(lst)):
        if lst[i] == key:
            return i
    return -1


lst = input('\nEnter the list of numbers: ')
lst = lst.split()
lst = [int(x) for x in lst]
key = int(input('The number to search for: '))

index = linear_search(lst, key)
if index < 0:
    print('{} was not found.'.format(key))
else:
    print('{} was found at index {}.'.format(key, index))
