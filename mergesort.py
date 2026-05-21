def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 測試
if __name__ == "__main__":
    test_cases = [
        [5, 2, 9, 1, 5, 6],
        [],
        [1],
        [3, 2, 1],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1]
    ]
    for arr in test_cases:
        sorted_arr = merge_sort(arr)
        print(f"原始: {arr} -> 排序後: {sorted_arr} -> 正確: {sorted_arr == sorted(arr)}")