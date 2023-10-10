import numpy as np

arr = np.full((6, 7), 'x')

def has_3_in_a_row(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            


            value = arr[i][j]



            if value == 0:
                continue
            # Check horizontal
            if j <= arr.shape[1] - 3 and all(arr[i, j:j+3] == value):
                return True
            # Check vertical
            if i <= arr.shape[0] - 3 and all(arr[i:i+3, j] == value):
                return True
            # Check diagonal
            if i <= arr.shape[0] - 3 and j <= arr.shape[1] - 3 and all(arr[i:i+3, j:j+3].diagonal() == value):
                return True
            # Check reverse diagonal
            if i >= 2 and j <= arr.shape[1] - 3 and all(np.fliplr(arr)[i-2:i+1, j:j+3].diagonal() == value):
                return True
    return False

print(has_3_in_a_row(arr)) # True
