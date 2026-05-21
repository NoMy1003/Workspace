from playwright.async_api import Page, TimeoutError, async_playwright
import asyncio
import logging
import time

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlaywrightXPathHelper:
    def __init__(self, page: Page, default_timeout: int = 8000):
        """
        初始化 Playwright XPath 輔助類
        
        Args:
            page: Playwright 頁面物件
            default_timeout: 預設等待時間（毫秒），預設為 8000ms (8秒)
        """
        self.page = page
        self.default_timeout = default_timeout
    
    def click_by_xpath(self, xpath: str, timeout: int = None) -> bool:
        """
        使用 XPath 定位元素並點擊
        
        Args:
            xpath: XPath 表達式
            timeout: 等待時間（毫秒），如果為 None 則使用預設值
            
        Returns:
            bool: 點擊成功返回 True，失敗返回 False
        """
        timeout = timeout or self.default_timeout
        
        try:
            logger.info(f"嘗試點擊元素，XPath: {xpath}")
            
            # 等待元素可見並可點擊
            element = self.page.wait_for_selector(
                f"xpath={xpath}", 
                timeout=timeout,
                state="visible"
            )
            
            # 確保元素可點擊
            element.wait_for_element_state("enabled", timeout=timeout)
            
            # 點擊元素
            element.click()
            
            logger.info(f"成功點擊元素，XPath: {xpath}")
            return True
            
        except TimeoutError:
            logger.error(f"等待元素超時，XPath: {xpath}，等待時間: {timeout}ms")
            return False
        except Exception as e:
            logger.error(f"點擊元素時發生錯誤，XPath: {xpath}，錯誤: {str(e)}")
            return False
    
    def input_by_xpath(self, xpath: str, text: str, timeout: int = None, clear_first: bool = True) -> bool:
        """
        使用 XPath 定位輸入框並輸入文字
        
        Args:
            xpath: XPath 表達式
            text: 要輸入的文字
            timeout: 等待時間（毫秒），如果為 None 則使用預設值
            clear_first: 是否先清空輸入框，預設為 True
            
        Returns:
            bool: 輸入成功返回 True，失敗返回 False
        """
        timeout = timeout or self.default_timeout
        
        try:
            logger.info(f"嘗試輸入文字到元素，XPath: {xpath}，文字: {text}")
            
            # 等待元素可見並可編輯
            element = self.page.wait_for_selector(
                f"xpath={xpath}", 
                timeout=timeout,
                state="visible"
            )
            
            # 確保元素可編輯
            element.wait_for_element_state("enabled", timeout=timeout)
            
            # 先清空輸入框（如果需要）
            #if clear_first:
            #    element.clear()
            
            # 輸入文字
            element.fill(text)
            
            logger.info(f"成功輸入文字到元素，XPath: {xpath}")
            return True
            
        except TimeoutError:
            logger.error(f"等待元素超時，XPath: {xpath}，等待時間: {timeout}ms")
            return False
        except Exception as e:
            logger.error(f"輸入文字時發生錯誤，XPath: {xpath}，錯誤: {str(e)}")
            return False
    
    def input_by_xpath_type(self, xpath: str, text: str, timeout: int = None, delay: int = 100) -> bool:
        """
        使用 XPath 定位輸入框並逐字輸入文字（模擬真實打字）
        
        Args:
            xpath: XPath 表達式
            text: 要輸入的文字
            timeout: 等待時間（毫秒），如果為 None 則使用預設值
            delay: 每個字符之間的延遲時間（毫秒），預設為 100ms
            
        Returns:
            bool: 輸入成功返回 True，失敗返回 False
        """
        timeout = timeout or self.default_timeout
        
        try:
            logger.info(f"嘗試逐字輸入文字到元素，XPath: {xpath}，文字: {text}")
            
            # 等待元素可見並可編輯
            element = self.page.wait_for_selector(
                f"xpath={xpath}", 
                timeout=timeout,
                state="visible"
            )
            
            # 確保元素可編輯
            element.wait_for_element_state("enabled", timeout=timeout)
            
            # 點擊元素以獲得焦點
            element.click()
            
            # 逐字輸入
            element.type(text, delay=delay)
            
            logger.info(f"成功逐字輸入文字到元素，XPath: {xpath}")
            return True
            
        except TimeoutError:
            logger.error(f"等待元素超時，XPath: {xpath}，等待時間: {timeout}ms")
            return False
        except Exception as e:
            logger.error(f"逐字輸入文字時發生錯誤，XPath: {xpath}，錯誤: {str(e)}")
            return False

# 使用範例
def example_usage():
    """
    使用範例
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 創建輔助類實例
        helper = PlaywrightXPathHelper(page, default_timeout=8000)
        
        try:
            # 導航到網頁
            page.goto("https://24h.pchome.com.tw/")
            time.sleep(5)
            
            # 使用 XPath 輸入文字
            success = helper.input_by_xpath("//form[@data-regression='header_search']//input[@type='search']", "iphone 16")
            if success:
                print("用戶名輸入成功")
            else:
                assert False, "用戶名稱輸入問題"
            
            # 使用 XPath 點擊按鈕
            success = helper.click_by_xpath("//button[@data-regression='header_search_button']")
            if success:
                print("按鈕點擊成功")
            else:
                assert False, "按鈕點擊失敗"
            
            time.sleep(10)
            
        finally:
            browser.close()

if __name__ == "__main__":
    example_usage()