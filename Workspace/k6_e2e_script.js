import http from 'k6/http';
import { check, sleep, group } from 'k6';

// 設定測試選項 (這部分與單一 API 測試一樣)
export const options = {
  stages: [
    { duration: '1m', target: 10 }, // 模擬 10 個使用者同時跑這個流程
  ],
};

export default function () {
  // 定義全域變數來存取跨請求的資料
  let authToken = '';
  let userId = '';

  // ============================================
  // 第一步：API A - 登入 (獲取 Token)
  // ============================================
  group('Step 1: Login', function () {
    const payload = JSON.stringify({
      username: 'myuser',
      password: 'mypassword',
    });
    
    const params = {
      headers: { 'Content-Type': 'application/json' },
    };

    const res = http.post('https://api.example.com/login', payload, params);

    // 【關鍵點】：驗證成功後，提取 Token
    const isLoginSuccess = check(res, {
      'Login status is 200': (r) => r.status === 200,
      'Token exists': (r) => r.json('token') !== undefined,
    });

    // 如果登入失敗，後面的流程跑了也沒意義，可以選擇報錯或略過
    if (isLoginSuccess) {
      authToken = res.json('token'); // 存入變數
    } else {
        console.error('Login Failed');
    }
  });

  // 模擬使用者思考時間 (重要！避免請求過於密集)
  sleep(1);

  // ============================================
  // 第二步：API B - 查詢資料 (使用 Token)
  // ============================================
  group('Step 2: Get User Profile', function () {
    // 【關鍵點】：將上一步的 authToken 帶入 Header
    const params = {
      headers: { 
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
    };

    const res = http.get('https://api.example.com/users/me', params);

    check(res, {
      'Profile status is 200': (r) => r.status === 200,
    });

    // 提取 UserId 供下一步使用
    userId = res.json('id'); 
  });

  sleep(2);

  // ============================================
  // 第三步：API C - 更新資料 (使用 Token + UserId)
  // ============================================
  group('Step 3: Update Profile', function () {
    const payload = JSON.stringify({
      bio: 'I am a K6 tester',
    });

    const params = {
      headers: { 
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      },
    };

    // 【關鍵點】：使用上一步取得的 userId 組出 URL
    const res = http.post(`https://api.example.com/users/${userId}/update`, payload, params);

    check(res, {
      'Update status is 200': (r) => r.status === 200,
    });
  });
  
  sleep(1);
}