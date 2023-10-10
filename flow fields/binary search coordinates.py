def binary_search_closest(x, arr):
    low = 0
    high = len(arr) - 1
    closest_index = None

    while low <= high:
        mid = (high + low) // 2

        # If x is greater, ignore left half
        if arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        elif arr[mid] > x:
            high = mid - 1

        # means x is present at mid
        else:
            return mid

        # Update closest_index if the current element is closer to x
        if closest_index is None or abs(arr[mid] - x) < abs(arr[closest_index] - x):
            closest_index = mid

    return closest_index

# Example usage:
arr = [1, 3, 5, 7, 9]
x = 6
closest_index = binary_search_closest(x, arr)
print("Closest index to", x, "is", arr[closest_index])
