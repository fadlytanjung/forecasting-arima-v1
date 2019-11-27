def maxDiff(arr):

    min_val = arr[0]
    max_diff = -1

    for i in range(1, len(arr)):

        if arr[i] <= min_val:
            min_val = arr[i]
        elif arr[i]-min_val > max_diff:
            max_diff = arr[i]-min_val

    return max_diff

arr = [2,6,20,1,18]
arr2 = [1,2,6,18,20]

def EncMaxDiff(arr):

    min_val = arr[0]
    max_val = arr[0]

    for i in range(1,len(arr)):
        if arr[i] > max_val:
            max_val = arr[i]
        elif arr[i] < min_val:
            min_val = arr[i]
        
    return max_val-min_val

# print(maxDiff(arr))
# print(EncMaxDiff(arr))

def minDiff(arr):

    min_val = arr[0]
    min_diff = 999999999999

    for i in range(1, len(arr)):

        if arr[i] <= min_val:
            min_val = arr[i]
        elif arr[i]-min_val < min_diff:
            min_diff = arr[i]-min_val

    return min_diff

# print(minDiff(arr2))

def EncMinDiff(arr):

    min_diff = 9999999999999999
    for i in range(len(arr)):
        for j in range(len(arr)):

            if arr[i]!=arr[j] and max(arr[i],arr[j])-min(arr[i],arr[j]) < min_diff:
                min_diff = max(arr[i], arr[j])-min(arr[i], arr[j])

    return min_diff

print(EncMinDiff(arr2))
