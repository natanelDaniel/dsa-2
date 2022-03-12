import numpy as np
import time
import matplotlib.pyplot as plt


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


def RandomizedQuickSort(A, p, r):
    if p<r:
        q = RandomizedPartition(A, p, r)
        RandomizedQuickSort(A, 0, q-1)
        RandomizedQuickSort(A, q+1, r)


def RandomizedPartition(A, p, r):
    f = np.random.randint(p, r)
    A[f], A[r] = A[r], A[f]
    return partition(A, p, r)


random_state1 = np.random.RandomState(101)
random_state2 = np.random.RandomState(101)
random_state3 = np.random.RandomState(101)

low = 0
high = 100
n = 50
random_array = random_state1.randint(low, high, n)

print("array to sort:", random_array)

startTime = time.time()
random_array.sort()
executionTime = (time.time() - startTime)
print('python sort Execution time in seconds: ' + str(executionTime))
print("sorted array:", random_array)


random_array = random_state2.randint(low, high, n)


startTime = time.time()
QuickSort(random_array, 0, n-1)
executionTime = (time.time() - startTime)
print('quick sort Execution time in seconds: ' + str(executionTime))
print("sorted array:", random_array)



"""random_array = random_state3.randint(low, high, n)
startTime = time.time()
RandomizedQuickSort(random_array, 0, n-1)
executionTime = (time.time() - startTime)
print('random quick sort Execution time in seconds: ' + str(executionTime))
print("sorted array:", random_array)"""

nums = []
time_python = []
time_quick_sort = []
for n in range(10, 100, 1):
    nums.append(n)
    low = 0
    high = 100

    random_array = random_state2.randint(low, high, n)
    startTime = time.time()
    QuickSort(random_array, 0, n-1)
    executionTime = (time.time() - startTime)
    time_quick_sort.append(executionTime)

    random_array = random_state1.randint(low, high, n)
    startTime = time.time()
    random_array.sort()
    executionTime = (time.time() - startTime)
    time_python.append(executionTime)

plt.plot(nums, time_python, label="python")
plt.plot(nums, time_quick_sort, label="quick sort")
plt.xlabel("numbers")
plt.ylabel("time[sec]")
plt.legend()
plt.show()

