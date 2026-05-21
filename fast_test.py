# 這是最基礎的 FastAPI 範例
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 定義一個 GET 請求，路徑是根目錄 "/"
@app.get("/")
def read_root():
    return {"message": "Hello, QA to Backend!"}

# 定義一個有參數的路徑
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    # 啟動伺服器
    uvicorn.run(app, host="127.0.0.1", port=8000)