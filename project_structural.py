import os
from google import genai
from google.genai import types # Gemini 的設定檔型態
from pydantic import BaseModel, Field
from typing import List

# 1. 初始化 Gemini 客戶端 (會自動讀取環境變數 GEMINI_API_KEY)
client = genai.Client(api_key="AIzaSyAco2yXH2pwNdUuPZzkHMC2CX0tDWh7DZA")

# 2. 定義資料結構 (與昨天完全相同，LLM 能直接看懂 Pydantic 的結構)
class TestStep(BaseModel):
    step_number: int
    action: str = Field(description="執行的動作，例如：點擊、輸入、檢查")
    target_element: str = Field(description="操作的目標物件，例如：登入按鈕、帳號輸入框")
    value: str = Field(description="輸入的數值或預期的檢查文字，若無則留空")

class TestCase(BaseModel):
    test_case_id: str
    title: str = Field(description="測試案例標題")
    precondition: str = Field(description="前置條件")
    steps: List[TestStep] = Field(description="詳細測試步驟列表")
    expected_result: str = Field(description="預期結果（斷言條件）")

class RequirementAnalysis(BaseModel):
    test_cases: List[TestCase]

# 模擬需求書
prd_document = """
需求名稱：會員登入功能變更
1. 使用者進入 /login 頁面。
2. 輸入電子郵件與密碼。電子郵件必須包含 @ 符號，密碼長度需大於 8 碼。
3. 點擊「登入」按鈕。
4. 若登入成功，系統應導向 /dashboard 首頁，並顯示「歡迎回來」的彈出訊息。
5. 若密碼少於 8 碼，輸入框下方應即時顯示紅字錯誤訊息「密碼長度不足」。
"""

# 3. 發送請求給 Gemini API
response = client.models.generate_content(
    model='gemini-2.5-flash', # 2026年標準主力模型，速度快且極度便宜
    contents=f"你是一位資深軟體測試專家（QA），請閱讀產品需求書（PRD），並將其拆解為多個涵蓋正向與逆向情境的測試案例：\n{prd_document}",
    config=types.GenerateContentConfig(
        # 告訴 Gemini 我們要 JSON，並且把 Pydantic 結構直接餵給它
        response_mime_type="application/json",
        response_schema=RequirementAnalysis,
        temperature=0.2 # 降低隨機性，讓產出的測試案例更嚴謹
    ),
)

# 4. 解析結果
# OpenAI 會自動幫你轉成物件，但 Gemini 回傳的是純文字 JSON 字串
# 我們需要手動用 Pydantic 的 model_validate_json 把它還原成 Python 物件



# 4. 解析結果
analyzed_data = RequirementAnalysis.model_validate_json(response.text)

print("--- Gemini 已成功生成結構化測試案例 ---")

# ==================== 💡 新增以下程式碼以產生實體檔案 ====================

# 1. 利用 Pydantic 內建方法，將記憶體中的物件轉換為帶有美化縮排（indent=2）的 JSON 字串
json_string = analyzed_data.model_dump_json(indent=2)

# 2. 指定你想生成的檔案名稱
output_filename = "test_cases.json"

# 3. 使用 Python 的 open 函數，將字串實際寫入硬碟
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(json_string)

# 4. 印出絕對路徑，方便你點擊查看
print(f"🎉 實體檔案已生成！路徑位於：{os.path.abspath(output_filename)}")