import json
import logging
import re
import ssl
from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
import urllib3

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class UnverifiedSSLAdapter(HTTPAdapter):
    """
    前因後果：為了解決 OpenSSL 3.0+ 對於不合規憑證（如缺少 Subject Key Identifier）
    會在 C 語言底層直接拋出 _ssl.c 錯誤的問題，在此建立極致放寬的 SSLContext。
    """
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            ctx.set_ciphers('DEFAULT@SECLEVEL=0')
        except Exception:
            pass
        return super().init_poolmanager(*args, **kwargs)


class APITester:
    def __init__(
        self,
        keep_alive: bool = True,
        timeout: int = 10,
        verify_ssl: bool = False,
        default_headers: Optional[Dict[str, str]] = None
    ):
        self.keep_alive = keep_alive
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        self.default_headers = default_headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python-APITester/1.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }

        # 1. 建立全局 Session
        self.session = requests.Session()

        # 2. 繞過 SSL 驗證與 OpenSSL 底層解析限制
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self.session.verify = False

            # 將強效 SSL 鬆綁適配器掛載至 https:// 與 http:// 協定
            ssl_adapter = UnverifiedSSLAdapter()
            self.session.mount("https://", ssl_adapter)
            self.session.mount("http://", ssl_adapter)

        # 全域變數與 Context
        self.last_response_text: str = ""
        self.last_response_json: Optional[Dict[str, Any]] = None
        self.last_response: Optional[requests.Response] = None
        self.context: Dict[str, Any] = {}

    def close(self):
        if self.session:
            self.session.close()

    def _replace_placeholders(self, target: Any) -> Any:
        """替換 {{var_name}} 佔位符"""
        if isinstance(target, str):
            matches = re.findall(r"\{\{\s*(\w+)\s*\}\}", target)
            for var in matches:
                if var in self.context:
                    target = target.replace(f"{{{{{var}}}}}", str(self.context[var]))
            return target
        elif isinstance(target, dict):
            return {k: self._replace_placeholders(v) for k, v in target.items()}
        elif isinstance(target, list):
            return [self._replace_placeholders(i) for i in target]
        return target

    def _deep_update(self, original: dict, override: dict) -> dict:
        """深度覆蓋字典：保留預設鍵、覆蓋重複鍵、自動新增新鍵"""
        result = dict(original or {})
        for k, v in (override or {}).items():
            if isinstance(v, dict) and k in result and isinstance(result[k], dict):
                result[k] = self._deep_update(result[k], v)
            else:
                result[k] = v
        return result

    def run_api(
        self,
        api_config: Dict[str, Any],
        api_name: str = "API_Test",
        override_payload: Optional[Dict[str, Any]] = None,
        override_headers: Optional[Dict[str, Any]] = None,
        override_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        # Header 繼承鏈處理：default_headers -> api_config.headers -> override_headers
        base_headers = self._deep_update(self.default_headers, api_config.get("headers") or {})
        final_headers = self._deep_update(base_headers, override_headers) if override_headers else base_headers

        base_payload = api_config.get("payload") or {}
        base_params = api_config.get("params") or {}

        final_payload = self._deep_update(base_payload, override_payload) if override_payload else base_payload
        final_params = self._deep_update(base_params, override_params) if override_params else base_params

        # 自動帶入變數池 {{var_name}}
        url = self._replace_placeholders(api_config.get("url", ""))
        method = api_config.get("method", "GET").upper()
        headers = self._replace_placeholders(final_headers)
        params = self._replace_placeholders(final_params)
        payload = self._replace_placeholders(final_payload)
        expect_status = api_config.get("expect_status", 200)
        expect_response = self._replace_placeholders(api_config.get("expect_response"))

        # 連線模式處理 (Non-keep-alive 補 Connection: close)
        if not self.keep_alive:
            headers["Connection"] = "close"

        logging.info(f"▶ 發送 API [{api_name}] ({method}) -> {url}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=payload if method in ["POST", "PUT", "PATCH"] else None,
                timeout=self.timeout
            )

            # 更新當下 Response 全域狀態
            self.last_response = response
            self.last_response_text = response.text
            try:
                self.last_response_json = response.json()
            except ValueError:
                self.last_response_json = None

        except requests.RequestException as e:
            self.last_response_text = ""
            self.last_response_json = None
            self.last_response = None
            return {"api_name": api_name, "passed": False, "error": f"網路請求異常: {str(e)}"}

        # 驗證 Status Code
        if response.status_code != expect_status:
            return {
                "api_name": api_name,
                "passed": False,
                "error": f"Status Code 錯誤！預期 {expect_status}，實際 {response.status_code}"
            }

        # 驗證 Expect Response 欄位比對
        if expect_response:
            if not self.last_response_json:
                return {"api_name": api_name, "passed": False, "error": "Response 非 JSON 格式，無法執行比對"}

            for k, v in expect_response.items():
                if k not in self.last_response_json or str(self.last_response_json[k]) != str(v):
                    return {
                        "api_name": api_name,
                        "passed": False,
                        "error": f"欄位 '{k}' 不符合！預期: '{v}'，實際: '{self.last_response_json.get(k)}'"
                    }

        return {"api_name": api_name, "passed": True, "error": None}

    def run_by_name(self, json_data: Dict[str, Any], api_name: str, **kwargs) -> Dict[str, Any]:
        if api_name not in json_data:
            raise KeyError(f"JSON 中找不到 key: '{api_name}'")
        return self.run_api(api_config=json_data[api_name], api_name=api_name, **kwargs)