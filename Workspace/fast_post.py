from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel

app = FastAPI()

# 1. 定義 Request Body 的資料結構 (Schema)
# 這就像是 QA 寫自動化測試時定義的 payload
class DocumentInput(BaseModel):
    title: str
    content: str
    is_top_secret: bool
    trigger_bug: bool = False  # 用來故意觸發 500 錯誤的開關

# 2. 定義 POST 請求
@app.post("/documents", status_code=status.HTTP_200_OK)
def create_document(
    document: DocumentInput,
    # 從 Header 讀取 Authorization 欄位，預設為 None
    authorization: str | None = Header(default=None)
):
    
    # --- 模擬 401 Unauthorized (未授權) ---
    # 情境：你連門票都沒有，我根本不知道你是誰。
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少認證 Token，請登入"
        )

    # --- 模擬 403 Forbidden (禁止訪問) ---
    # 情境：我知道你是誰（你有票），但你等級不夠，不能進去 VIP 包廂。
    # 這裡假設 Token 是 "guest_token"，但試圖上傳機密文件 (is_top_secret=True)
    if authorization == "guest_token" and document.is_top_secret:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您的權限不足，無法建立機密文件"
        )

    # --- 模擬 500 Internal Server Error (伺服器內部錯誤) ---
    # 情境：程式碼寫壞了，或者資料庫突然斷線。這是後端工程師最不想看到的錯誤。
    # 這裡我們用一個變數故意觸發「除以零」的崩潰，模擬非預期的錯誤
    if document.trigger_bug:
        # 通常我們不會手動 raise 500，500 是程式崩潰時自動發生的
        # 這裡模擬程式邏輯出錯
        x = 1 / 0 
        
    # --- 模擬 200 OK (成功) ---
    # 所有檢查都通過，回傳成功結果
    return {
        "status": "success",
        "message": f"文件 '{document.title}' 建立成功",
        "owner": authorization
    }