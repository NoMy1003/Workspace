def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)

# --- 範例測試 ---
test1 = [3,6,8,10,1,2,1]
sorted_test1 = quicksort(test1)
print(sorted_test1)  # Output: [1, 1, 2, 3, 6, 8, 10]