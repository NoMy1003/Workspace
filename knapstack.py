def knapsack_dp(weights, values, W):
    """
    使用動態規劃解決 0/1 背包問題

    :param weights: 物品重量列表 (list of int)
    :param values: 物品價值列表 (list of int)
    :param W: 背包最大容量 (int)
    :return: 可獲得的最大總價值 (int)
    """
    N = len(weights)
    
    # 建立一個 (N+1) x (W+1) 的 DP 表，並初始化為 0
    # dp[i][w] 代表考慮前 i 個物品，在容量 w 下的最大價值
    dp = [[0 for _ in range(W + 1)] for _ in range(N + 1)]
    
    # 開始填表，i 代表考慮到第 i 個物品
    for i in range(1, N + 1):
        # w 代表當前的背包容量
        for w in range(1, W + 1):
            # 物品索引是 i-1，因為物品列表從 0 開始
            item_weight = weights[i - 1]
            item_value = values[i - 1]
            
            # 如果當前物品的重量大於背包容量 w，則無法放入
            if item_weight > w:
                # 價值等於不放此物品的價值，即與前 i-1 個物品的狀態相同
                dp[i][w] = dp[i - 1][w]
            else:
                # 如果可以放入，我們需要在「不放」和「放」之間做選擇
                # 1. 不放第 i 個物品的價值
                value_without_item = dp[i - 1][w]
                
                # 2. 放第 i 個物品的價值
                value_with_item = item_value + dp[i - 1][w - item_weight]
                
                # 取兩者中的最大值
                dp[i][w] = max(value_without_item, value_with_item)
                
    # DP 表的右下角即為最終答案
    return dp[N][W]

# --- 範例測試 ---
weights = [1, 2, 3]    # 物品重量
values = [10, 15, 40]  # 物品價值
W = 6                  # 背包最大容量

max_value = knapsack_dp(weights, values, W)
print(f"背包能裝下的最大價值為: {max_value}")

# 範例解釋：
# 物品1: 重量 1, 價值 10
# 物品2: 重量 2, 價值 15
# 物品3: 重量 3, 價值 40
# 背包容量: 6
#
# 最優解是選擇物品2和物品3 (重量 2+3=5 <= 6)，總價值 15+40=55。
# 讓我們看看程式是否能跑出 55。
# 喔，等等，如果選物品1和物品3，重量是1+3=4，價值是10+40=50
# 如果選物品3和...等等，最佳解應該是物品3(重量3)+物品?(重量3)=總重6 => 價值 40+15=55? 不對，是物品3(3,40)+物品2(2,15)+物品1(1,10)，總重為6，價值65
# 讓我們用上面的例子手動跑一次
# W=6, N=3
# weights=[1,2,3], values=[10,15,40]
# 最優解應為放入全部物品，重量 1+2+3=6，價值 10+15+40=65
# 程式應該要輸出 65

weights_test = [3, 2, 1]
values_test = [40, 15, 10]
W_test = 6
max_value_test = knapsack_dp(weights_test, values_test, W_test)
print(f"背包能裝下的最大價值為(驗證): {max_value_test}")

