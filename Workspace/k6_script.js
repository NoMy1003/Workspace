import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. 設定測試情境 (Options)
// 這裡定義了負載模型，這是效能測試的「心臟」。
export const options = {
  // 定義三個階段 (Stages)
  stages: [
    { duration: '30s', target: 20 }, // Ramp-up: 前30秒，使用者從 0 增加到 20 人
    { duration: '1m',  target: 20 }, // Load: 接下來1分鐘，維持 20 人同時在線
    { duration: '10s', target: 0 },  // Ramp-down: 最後10秒，人數降回 0
  ],
  
  // 定義成功標準 (Thresholds)
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% 的請求回應時間必須小於 500ms
    http_req_failed: ['rate<0.01'],   // 失敗率必須低於 1%
  },
};

// 2. 虛擬使用者的行為 (The Scenario)
// 這裡的 function 會被每個 VU 不斷重複執行
export default function () {
  // 發送 GET 請求 (這裡暫用 k6 官方測試站)
  const res = http.get('https://test.k6.io');

  // 3. 驗證回應 (Checks)
  // 這只是為了確認 API 功能正常，不是效能指標
  check(res, {
    'status is 200': (r) => r.status === 200,
    'protocol is HTTP/2': (r) => r.proto === 'HTTP/2.0',
  });

  // 4. 思考時間 (Think Time)
  // 非常重要！真實使用者不會一秒鐘點擊 100 次。
  // sleep(1) 代表使用者看完頁面停頓 1 秒才做下個動作。
  sleep(1);
}

// 5. 執行測試
// 在終端機中執行以下指令來啟動測試：
// k6 run k6_script.js
//
// 6. 分析結果
// 測試結束後，k6 會在終端機中顯示詳細的效能報告，
// 包含請求數量、失敗率、回應時間分佈等資訊。
// 根據這些數據，你可以評估系統在不同負載下的表現，
// 並找出潛在的瓶頸與改進空間。