def bubble_sort(l):
    # Swap the elements to arrange in order
    for iter_num in range(len(l) - 1, 0, -1):
        for i in range(iter_num):
            if l[i] > l[i + 1]:
                temp = l[i]
                l[i] = l[i + 1]
                l[i + 1] = temp


l = [19, 2, 31, 45, 6, 11, 121, 27]
bubble_sort(l)
print()
print(l)
