import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binom

# 設定支援繁體中文的字體 (視您的作業系統可微調為 'Microsoft JhengHei' 或 'PingFang HK')
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang HK', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 參數設定
n_users = 20
# 建立 X 軸數據：0.5 到 8.0 小時，並特別插入 2.4 小時 (30%) 作為關鍵觀測點
hours = np.array([0.5, 1.0, 1.5, 2.0, 2.4, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0])
p_values = hours / 8.0

# 二項式累積機率計算 (超過授權數的機率)
prob_10 = (1 - binom.cdf(10, n_users, p_values)) * 100
prob_11 = (1 - binom.cdf(11, n_users, p_values)) * 100
prob_12 = (1 - binom.cdf(12, n_users, p_values)) * 100
prob_13 = (1 - binom.cdf(13, n_users, p_values)) * 100
prob_14 = (1 - binom.cdf(14, n_users, p_values)) * 100
prob_15 = (1 - binom.cdf(15, n_users, p_values)) * 100

# 開始繪圖，設定畫布大小以確保比例與您上傳的圖片一致
plt.figure(figsize=(16, 7))

# 繪製三條折線，完美復刻您的顏色與標記 (Marker)
plt.plot(hours, prob_10, marker='o', color='#3498DB', linewidth=2.5, markersize=7, label='10 個授權 (10 Licenses)')
plt.plot(hours, prob_11, marker='s', color='#9B59B6', linewidth=2.5, markersize=7, label='11 個授權 (11 Licenses)')
plt.plot(hours, prob_12, marker='^', color="#BCB71A", linewidth=2.5, markersize=7, label='12 個授權 (12 Licenses)')
plt.plot(hours, prob_13, marker='o', color='#E74C3C', linewidth=2.5, markersize=7, label='13 個授權 (13 Licenses)')
plt.plot(hours, prob_14, marker='s', color='#F39C12', linewidth=2.5, markersize=7, label='14 個授權 (14 Licenses)')
plt.plot(hours, prob_15, marker='^', color='#2ECC71', linewidth=2.5, markersize=7, label='15 個授權 (15 Licenses)')

# 標題與座標軸標籤
plt.title('UiPath 授權衝突機率分析：依據使用者日均使用時間 (總人數 30 人)', fontsize=16, pad=20)
plt.xlabel('每位使用者平均日使用時數 (X軸：0.5 ~ 8.0 小時，每半小時一節點)', fontsize=13)
plt.ylabel('發生授權不足而進入 Pending 的機率 (%)', fontsize=13)

# 設定 X 軸與 Y 軸的刻度
plt.xticks(np.arange(0.5, 8.5, 0.5), fontsize=11)
plt.yticks(np.arange(0, 101, 10), fontsize=11)

# 加入網格線
plt.grid(True, linestyle='--', alpha=0.6, color='#BDC3C7')

# 加入圖例
plt.legend(loc='upper left', fontsize=11, framealpha=0.9)

# (選用) 特別標註 30% 基準線，增強簡報說服力
plt.axvline(x=2.4, color='#7F8C8D', linestyle=':', alpha=0.8, linewidth=2)
plt.text(2.45, 90, 'IT 實際使用率基準\n(30% / 2.4小時)', color='#7F8C8D', fontsize=11, weight='bold')

# 自動調整佈局並顯示
plt.tight_layout()
plt.show()