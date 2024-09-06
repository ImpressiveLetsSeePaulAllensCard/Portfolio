"""
Sorting Algorithms
Implementation of:
Bubble Sort
Insertion Sort
Merge Sort
Hybrid Sort (Call Merge or Hybrid Sort based on the list size)
Quick Sort
Radix Sort
Author: Alyx Stockton
"""


import time
import random
import sys
from math import ceil, log10

sys.setrecursionlimit(100000)


def bubbleSort(alist):
    """
    Implementation of Bubble Sort
    Using a nested for loop, compare values side by side
    Swap if the value on left is greater than value on the right
    Perform again going up to the n-1 element
    Perform until we reach the n-n iteration
    """
    start_time = time.time()

    # Beginning of implementation
    n = len(alist)

    for i in range(n):
        for j in range(0, n - i - 1):
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]

    elapsed_time = time.time() - start_time

    return (alist, elapsed_time)


def insertionSort(alist):
    """
    Implementation of insertion sort
    Pick the second element of our list and compare it to the first element. If element 1 is greater, swap them.
    If no swap is needed, we already have a sorted subarray.
    Proceed to go through our unsorted subarray and place all of the elements in the correct spot in the sorted subarray
    Each subsequent element essentially functions as a "key" to insert
    Go until we reach the final element in the list
    """
    start_time = time.time()

    for i in range(1, len(alist)):
        key = alist[i]
        j = i - 1

        while j >= 0 and key < alist[j]:
            alist[j + 1] = alist[j]
            j -= 1
            alist[j + 1] = key

    elapsed_time = time.time() - start_time
    return (alist, elapsed_time)


def mergeSort(alist):
    """
    Actual merge sort function, broken up
    Start by calling the helper function
    We should have a sorted list by the time by the helper functions return
    """
    start_time = time.time()
    sorted_list = mergeSortHelper(alist)
    elapsed_time = time.time() - start_time
    return (sorted_list, elapsed_time)


def mergeSortHelper(alist):
    """
    First helper function for merge sort
    Recursively call this function on our array until we have n sub arrays
    Call the merge helper function which sorts our two subarrays

    """
    if len(alist) > 1:
        mid = len(alist) // 2
        left_half = alist[:mid]
        right_half = alist[mid:]

        # Recursive Call to sort the two halves
        mergeSortHelper(left_half)
        mergeSortHelper(right_half)

        merge(alist, left_half, right_half)
    return alist


def merge(alist, left_half, right_half):
    """
    Helper function designed to merge the two subarrays
    Compare elements from each subarray and place the smaller element in the correct spot
    """
    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            alist[k] = left_half[i]
            i += 1
        else:
            alist[k] = right_half[j]
            j += 1
        k += 1

    # Add elements left from subarrays (if any)
    while i < len(left_half):
        alist[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        alist[k] = right_half[j]
        j += 1
        k += 1


def hybridSort(alist):
    """
    Hybrid sort implementation
    Call merge or insertion sort based on the list size
    """
    start_time = time.time()

    n = len(alist)

    if n < 100:
        alist = insertionSort(alist)[0]
    else:
        alist = mergeSort(alist)[0]
    elapsed_time = time.time() - start_time
    return (alist, elapsed_time)


def quickSort(alist, pivot='first'):
    """
    Quick sort implementation
    pick a pivot based on the the parameter
    Rearrange all other elements around the pivot
    If pivot = "Middle", call partition with the middle element
    If pivot = "First", pivet index is set as 0
    """
    start_time = time.time()
    if len(alist) <= 1:
        elapsed_time = time.time() - start_time
        return (alist, elapsed_time)

    if pivot == 'middle':
        pivot_index = len(alist) // 2
    else:
        pivot_index = 0

    pivot_index = partition(alist, 0, len(alist) - 1, pivot_index)

    left_arr = alist[:pivot_index]
    right_arr = alist[pivot_index + 1:]

    # Recursive calls for the left and right partitions
    left_arr, _ = quickSort(left_arr, pivot)
    right_arr, _ = quickSort(right_arr, pivot)

    elapsed_time = time.time() - start_time
    return (left_arr + [alist[pivot_index]] + right_arr, elapsed_time)


def partition(arr, low, high, pivot_index):
    """
    Helper function for partitioning the elements of the array
    Rearrange the elements of our array based off the value of the pivot
    """
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]
    pivot = arr[low]
    left = low + 1
    right = high

    done = False
    while not done:
        while left <= right and arr[left] <= pivot:
            left = left + 1
        while arr[right] >= pivot and right >= left:
            right = right - 1
        if right < left:
            done = True
        else:
            # Swap arr[left] and arr[right]
            arr[left], arr[right] = arr[right], arr[left]

    # Swap arr[low] (pivot) and arr[right]
    arr[low], arr[right] = arr[right], arr[low]

    return right


def radixSort(alist):
    """
    Finally we have radix sort
    Useful for multidigit numbers
    Start with the least significant digits spot and sort all the values based on that
    Then move on to the next digits spot and repeat the same process
    Then repeat the same process one last time for the ones digit place and you will have a list that is sorted
    """
    start_time = time.time()

    max_digits = len(str(max(alist)))

    buckets = [[] for _ in range(10)]

    for digit_position in range(max_digits):
        for num in alist:
            digit_value = (num // (10 ** digit_position)) % 10
            buckets[digit_value].append(num)

        alist.clear()
        for bucket in buckets:
            alist.extend(bucket)
            bucket.clear()

    elapsed_time = time.time() - start_time
    return (alist, elapsed_time)


if __name__ == '__main__':
    """ Check if the program is being run directly (i.e. not being imported) """
    result_ceil = ceil(4.2)
    result_log10 = log10(100)

    def testFunction(sort_function, alist):
        """ A test utility function. """
        alist2 = alist.copy()
        res = sort_function(list(alist))
        print(f"Using {sort_function.__name__} to sort list: {alist[:10]}... w/ {len(alist)} items")
        print(f"    sort time: {res[1]:.4f} seconds")
        alist2.sort()
        print(f"    sorted correctly?: {'y :)' if res[0] == alist2 else 'n :('}")

    list1 = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    testFunction(bubbleSort, list(list1))
    testFunction(insertionSort, list(list1))
    testFunction(mergeSort, list(list1))
    testFunction(hybridSort, list(list1))
    testFunction(quickSort, list(list1))
    testFunction(radixSort, list(list1))

    random.seed(1)
    list2 = list(range(5000))
    random.shuffle(list2)
    testFunction(bubbleSort, list(list2))
    testFunction(insertionSort, list(list2))
    testFunction(mergeSort, list(list2))
    testFunction(hybridSort, list(list2))
    testFunction(quickSort, list(list2))
    testFunction(radixSort, list(list2))

    list3 = list(range(6000, 1000, -1))
    testFunction(bubbleSort, list(list3))
    testFunction(insertionSort, list(list3))
    testFunction(mergeSort, list(list3))
    testFunction(hybridSort, list(list3))
    testFunction(quickSort, list(list3))
    testFunction(radixSort, list(list3))
