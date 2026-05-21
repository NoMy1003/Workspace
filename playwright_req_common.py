import json
from typing import Optional, Dict, Any, Union
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright

class APIClient:
    """
    增強版 Playwright API 客戶端類別
    支援預設標頭、用戶 token 和 URL 參數處理
    """
    
    def __init__(self, base_url: str = "", default_headers: Optional[Dict[str, str]] = None, user_token: Optional[str] = None):
        """
        初始化 API 客戶端
        
        Args:
            base_url (str): API 基礎 URL
            default_headers (Optional[Dict]): 預設請求標頭
            user_token (Optional[str]): 用戶認證 token
        """
        self.base_url = base_url.rstrip('/')
        self.default_headers = default_headers or {}
        self.user_token = user_token
        
        # 如果有 token，自動添加到預設標頭
        if self.user_token:
            self.default_headers['Authorization'] = f'Bearer {self.user_token}'
    
    def set_token(self, token: str):
        """設定或更新用戶 token"""
        self.user_token = token
        self.default_headers['Authorization'] = f'Bearer {token}'
    
    def remove_token(self):
        """移除用戶 token"""
        self.user_token = None
        if 'Authorization' in self.default_headers:
            del self.default_headers['Authorization']
    
    def api_request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30000,
        use_full_url: bool = False
    ) -> Dict[str, Any]:
        """
        發送 API 請求的通用函式
        
        Args:
            method (str): HTTP 方法 (GET, POST, PUT, PATCH, DELETE)
            endpoint (str): API 端點路徑或完整 URL
            payload (Optional[Dict]): 請求資料 (JSON 格式)
            headers (Optional[Dict]): 額外的請求標頭
            params (Optional[Dict]): URL 查詢參數
            timeout (int): 請求超時時間 (毫秒)
            use_full_url (bool): 是否使用完整 URL (忽略 base_url)
        
        Returns:
            Dict[str, Any]: 包含狀態碼、回應資料和錯誤訊息的字典
        """
        
        # 標準化 HTTP 方法
        method = method.upper()
        
        # 驗證 HTTP 方法
        valid_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if method not in valid_methods:
            return {
                'success': False,
                'status_code': None,
                'data': None,
                'error': f'不支援的 HTTP 方法: {method}. 支援的方法: {valid_methods}'
            }
        
        # 建構完整 URL
        if use_full_url or endpoint.startswith(('http://', 'https://')):
            url = endpoint
        else:
            url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint
        
        # 處理 URL 參數
        if params:
            separator = '&' if '?' in url else '?'
            url += separator + urlencode(params)
        
        # 合併標頭 (預設標頭 + 自訂標頭)
        merged_headers = self.default_headers.copy()
        if headers:
            merged_headers.update(headers)
        
        # 自動判斷是否需要 payload
        methods_with_payload = ['POST', 'PUT', 'PATCH']
        
        try:
            with sync_playwright() as p:
                # 建立請求上下文
                request_context = p.request.new_context()
                
                # 準備請求參數
                request_kwargs = {
                    'url': url,
                    'timeout': timeout
                }
                
                # 添加標頭
                if merged_headers:
                    request_kwargs['headers'] = merged_headers
                
                # 根據方法類型決定是否添加 payload
                if method in methods_with_payload and payload is not None:
                    request_kwargs['data'] = json.dumps(payload)
                    # 確保 Content-Type 為 application/json
                    if 'headers' not in request_kwargs:
                        request_kwargs['headers'] = {}
                    if 'Content-Type' not in request_kwargs['headers']:
                        request_kwargs['headers']['Content-Type'] = 'application/json'
                
                # 發送請求
                if method == 'GET':
                    response = request_context.get(**request_kwargs)
                elif method == 'POST':
                    response = request_context.post(**request_kwargs)
                elif method == 'PUT':
                    response = request_context.put(**request_kwargs)
                elif method == 'PATCH':
                    response = request_context.patch(**request_kwargs)
                elif method == 'DELETE':
                    response = request_context.delete(**request_kwargs)
                
                # 處理回應
                try:
                    response_data = response.json()
                except:
                    # 如果無法解析為 JSON，返回文字內容
                    response_data = response.text()
                
                return {
                    'success': response.ok,
                    'status_code': response.status,
                    'data': response_data,
                    'error': None if response.ok else f'HTTP {response.status}: {response.status_text}',
                    'url': url  # 返回實際請求的 URL
                }
                
        except Exception as e:
            return {
                'success': False,
                'status_code': None,
                'data': None,
                'error': f'請求失敗: {str(e)}',
                'url': url
            }

# 便利函式版本 (保持向後相容)
def api_request(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30000
) -> Dict[str, Any]:
    """
    簡化版 API 請求函式 (向後相容)
    """
    client = APIClient()
    return client.api_request(
        method=method,
        endpoint=url,
        payload=payload,
        headers=headers,
        params=params,
        timeout=timeout,
        use_full_url=True
    )

# 使用範例
def example_usage():
    """示範如何使用增強版 API 客戶端"""
    
    # 方法 1: 使用 APIClient 類別 (推薦)
    print("=== 使用 APIClient 類別 ===")
    
    # 初始化客戶端，設定基礎 URL 和預設標頭
    client = APIClient(
        base_url="https://httpbin.org",
        default_headers={
            "User-Agent": "MyApp/1.0",
            "Accept": "application/json"
        },
        user_token="your-jwt-token-here"
    )
    
    # GET 請求帶參數
    print("\n--- GET 請求帶參數 ---")
    result = client.api_request(
        'GET', 
        '/get',
        params={'page': 1, 'limit': 10, 'search': '測試'}
    )
    print(f"狀態: {result['success']}")
    print(f"實際 URL: {result['url']}")
    
    # POST 請求
    print("\n--- POST 請求 ---")
    post_data = {
        'name': '張三',
        'email': 'zhang@example.com',
        'age': 30
    }
    result = client.api_request('POST', '/post', payload=post_data)
    print(f"狀態: {result['success']}")
    print(f"狀態碼: {result['status_code']}")
    
    # PUT 請求帶額外標頭
    print("\n--- PUT 請求帶額外標頭 ---")
    put_data = {
        'id': 123,
        'name': '李四',
        'email': 'li@example.com'
    }
    extra_headers = {
        'X-Request-ID': 'req-12345',
        'X-Client-Version': '2.0'
    }
    result = client.api_request(
        'PUT', 
        '/put', 
        payload=put_data,
        headers=extra_headers
    )
    print(f"狀態: {result['success']}")
    
    # 更新 token
    print("\n--- 更新 token ---")
    client.set_token("new-jwt-token")
    result = client.api_request('GET', '/bearer')
    print(f"狀態: {result['success']}")
    
    # 方法 2: 使用便利函式 (向後相容)
    print("\n=== 使用便利函式 ===")
    result = api_request(
        'GET',
        'https://httpbin.org/get',
        params={'test': 'value'}
    )
    print(f"狀態: {result['success']}")

# 實際應用範例：完整的 API 流程
def real_world_example():
    """真實世界的 API 使用範例"""
    
    # 初始化 API 客戶端
    api = APIClient(
        base_url="https://jsonplaceholder.typicode.com",
        default_headers={
            "Content-Type": "application/json",
            "User-Agent": "MyTestApp/1.0"
        }
    )
    
    print("=== 真實世界範例：部落格 API ===")
    
    # 1. 獲取所有文章 (帶分頁參數)
    print("\n1. 獲取文章列表")
    posts_result = api.api_request(
        'GET',
        '/posts',
        params={'_page': 1, '_limit': 5}
    )
    
    if posts_result['success']:
        posts = posts_result['data']
        print(f"成功獲取 {len(posts)} 篇文章")
        first_post_id = posts[0]['id'] if posts else None
    else:
        print(f"獲取文章失敗: {posts_result['error']}")
        return
    
    # 2. 獲取特定文章
    if first_post_id:
        print(f"\n2. 獲取文章 ID {first_post_id}")
        post_result = api.api_request('GET', f'/posts/{first_post_id}')
        
        if post_result['success']:
            post = post_result['data']
            print(f"文章標題: {post['title']}")
        else:
            print(f"獲取文章失敗: {post_result['error']}")
    
    # 3. 建立新文章
    print("\n3. 建立新文章")
    new_post = {
        'title': '我的測試文章',
        'body': '這是一篇測試文章的內容',
        'userId': 1
    }
    
    create_result = api.api_request('POST', '/posts', payload=new_post)
    
    if create_result['success']:
        created_post = create_result['data']
        print(f"成功建立文章，ID: {created_post['id']}")
        
        # 4. 更新文章
        print("\n4. 更新文章")
        updated_post = {
            'id': created_post['id'],
            'title': '更新後的文章標題',
            'body': '更新後的文章內容',
            'userId': 1
        }
        
        update_result = api.api_request(
            'PUT',
            f'/posts/{created_post["id"]}',
            payload=updated_post
        )
        
        if update_result['success']:
            print("文章更新成功")
        else:
            print(f"更新失敗: {update_result['error']}")
        
        # 5. 刪除文章
        print("\n5. 刪除文章")
        delete_result = api.api_request('DELETE', f'/posts/{created_post["id"]}')
        
        if delete_result['success']:
            print("文章刪除成功")
        else:
            print(f"刪除失敗: {delete_result['error']}")
    else:
        print(f"建立文章失敗: {create_result['error']}")

if __name__ == "__main__":
    # 執行範例
    example_usage()
    print("\n" + "="*60)
    real_world_example()