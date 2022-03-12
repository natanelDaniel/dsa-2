import numpy as np
import time
import matplotlib.pyplot as plt
import statistics

def QuickSort(A, p, r):
    if p<r:
        q = partition(A, p, r)
        QuickSort(A, 0, q-1)
        QuickSort(A, q+1, r)

def partition(A, p, r):
    x = A[r]
    i = p-1
    for j in range(p, r):
        if A[j] <=x:
            i+=1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r],A[i+1]
    return i+1


def find_median_naive(array):
    array.sort()
    if not len(array):
        return None
    if len(array) % 2:
        return array[(len(array)//2)-1]
    return array[(len(array)//2)]

def find_k_naive(array, k):
    if not len(array):
        return None
    QuickSort(array, 0, len(array)-1)
    return array[k-1]


def select(array, k):
    if len(array) < 140:
        return find_k_naive(array, k)
    array_of_5 = []
    i = 0
    while i < len(array):
        j = 0
        array_of_5.append([])
        while j < 5 and i < len(array):
            array_of_5[-1].append(array[i])
            i += 1
            j += 1
    b = []
    for five in array_of_5:
        b.append(statistics.median(five))
    x = select(b, len(b)//2 - 1)
    l = []
    r = []
    for a in array:
        if a <= x:
            l.append(a)
        else:
            r.append(a)
    if k <= len(l):
        return select(l, k)
    return select(r, k-len(l))



random_state1 = np.random.RandomState(101)
random_state2 = np.random.RandomState(101)
a1 = random_state1.randint(0, 1000, 404)
a2 = random_state2.randint(0, 1000, 404)
print(a1)
startTime = time.time()
print(select(a1, 10))
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


startTime = time.time()
print(find_k_naive(a2, 10))
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
