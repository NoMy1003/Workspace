import math

def introsort(arr):
    # 計算最大遞迴深度限制：2 * log2(n)
    max_depth = 2 * math.floor(math.log2(len(arr)))
    _introsort(arr, 0, len(arr) - 1, max_depth)

def _introsort(arr, start, end, depth_limit):
    size = end - start + 1
    
    # 1. 數據量小的時候，用 Insertion Sort 收尾
    if size < 16:
        insertion_sort(arr, start, end)
        return

    # 2. 遞迴深度太深，切換成 Heapsort 避免 O(n^2)
    if depth_limit == 0:
        heapsort(arr, start, end)
        return

    # 3. 標準 Quicksort 流程
    pivot = partition(arr, start, end)
    _introsort(arr, start, pivot - 1, depth_limit - 1)
    _introsort(arr, pivot + 1, end, depth_limit - 1)

# --- 輔助函式 (僅列出概念) ---

def insertion_sort(arr, start, end):
    for i in range(start + 1, end + 1):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def partition(arr, low, high):
    # 這裡通常會用 Median-of-three 來選 Pivot
    pivot = arr[high] 
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def heapsort(arr, start, end):
    # 建立 Heap 並排序的邏輯 (使用 python heapq 或手寫)
    # 為了簡化，這裡示意用標準庫模擬
    temp = arr[start:end+1]
    import heapq
    heapq.heapify(temp)
    for i in range(start, end+1):
        arr[i] = heapq.heappop(temp)

# --- 範例測試 ---
##Bigger matrix
test1 = [i for i in range(10000, 0, -2)]
introsort(test1)
print(test1)