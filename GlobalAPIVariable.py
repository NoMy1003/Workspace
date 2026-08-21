FubonAppResult = {
    "flowId": None,
    "captcha_png_base64": None,
    "login_token": None,
    "temp_access_token": None,
    "disposable_token": None,
    "access_token": None,
    "response_text": None,
    "cookie": None
}

def InitializeData(target_dict: dict):
    """
    將傳入字典底下的所有 Value 歸零/清空為 None (採原地修改，維持記憶體位址一致)
    """
    if not isinstance(target_dict, dict):
        return

    for key in target_dict:
        # 若未來 Value 裡面還有巢狀 Dict，也可遞迴清空；一般狀況直接設為 None 即可
        if isinstance(target_dict[key], dict):
            InitializeData(target_dict[key])
        else:
            target_dict[key] = None