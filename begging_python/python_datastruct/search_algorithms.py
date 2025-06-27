from operator import le
import random


def binarySearch(target, sortedLyst):
    left = 0
    right = len(sortedLyst) - 1
    count = 0
    while left <= right:
        midpoint = (left + right) // 2
        count += 1
        print(count, " time:left, mid, right", sortedLyst[left],
              sortedLyst[midpoint], sortedLyst[right])
        if target == sortedLyst[midpoint]:
            return midpoint
        elif target < sortedLyst[midpoint]:
            right = midpoint - 1
        else:
            left = midpoint + 1
    return -1


#a = [20, 44, 48, 55, 62, 66, 74, 88, 93, 99]
#print(binarySearch(44, a))
def swap(lyst, i, j):
    lyst[i], lyst[j] = lyst[j], lyst[i]


def quicksort(lyst):
    quicksortHelper(lyst, 0, len(lyst) - 1)


def quicksortHelper(lyst, left, right):
    if left < right:
        pivotLocation = partition(lyst, left, right)
        quicksortHelper(lyst, left, pivotLocation - 1)
        quicksortHelper(lyst, pivotLocation + 1, right)


def partition(lyst, left, right):
    middle = (left + right) // 2
    pivot = lyst[middle]
    lyst[middle] = lyst[right]
    lyst[right] = pivot
    boundary = left
    for index in range(left, right):
        if lyst[index] < pivot:
            swap(lyst, index, boundary)
            boundary += 1
    swap(lyst, right, boundary)
    return boundary


if __name__ == "__main__":
    lyst = []
    size = 20
    for count in range(size):
        lyst.append(random.randint(1, size + 1))
    print(lyst)
    quicksort(lyst)
    print(lyst)