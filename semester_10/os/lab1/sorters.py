from statistic import Comparator, Assigner


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if Comparator.compare_more(arr[j], arr[j + 1]):
                Assigner.swap(arr, j, j + 1)
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and Comparator.compare_less(key, arr[j]):
            Assigner.assign(arr, j + 1, arr[j])
            j -= 1
        Assigner.assign(arr, j + 1, key)
    return arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        left = arr[:mid]  # Dividing the array elements
        right = arr[mid:]  # into 2 halves

        merge_sort(left)  # Sorting the first half
        merge_sort(right)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays left[] and right[]
        while i < len(left) and j < len(right):
            if Comparator.compare_less(left[i], right[j]):
                Assigner.assign(arr, k, left[i])
                i += 1
            else:
                Assigner.assign(arr, k, right[j])
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left):
            Assigner.assign(arr, k, left[i])
            i += 1
            k += 1

        while j < len(right):
            Assigner.assign(arr, k, right[j])
            j += 1
            k += 1
    return arr


def __partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        if Comparator.compare_less_or_eq(arr[j], pivot):
            i += 1
            Assigner.swap(arr, i, j)

    Assigner.swap(arr, i + 1, high)
    return i + 1


def __quick_sort(arr, low, high):
    if low < high:
        pi = __partition(arr, low, high)

        __quick_sort(arr, low, pi - 1)
        __quick_sort(arr, pi + 1, high)
    return arr


def quick_sort(arr):
    return __quick_sort(arr, 0, len(arr) - 1)
