import requests
from lxml import html

# 目標網址
url = 'https://example.com'

# 發送 GET 請求
response = requests.get(url)
response.raise_for_status()  # 檢查請求是否成功

# 解析 HTML
tree = html.fromstring(response.content)

# 以 XPath 選取你想要的資料（這裡以標題為例）
titles = tree.xpath('//h1/text()')

for title in titles:
    print(title)