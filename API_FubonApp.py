import json
import base64
import ddddocr
from ApiTester import APITester
import GlobalAPIVariable

class FubonAppClient:
    def __init__(self, keep_alive=True, verify_ssl=False):
        self.tester = APITester(keep_alive=keep_alive, verify_ssl=verify_ssl)

    def Logout(self, arg):
        keep_alive = arg.get("keep_alive", True)
        with open("FubonApp.json", "r", encoding="utf-8") as file:
            json_to_be_tested = json.load(file)

        if keep_alive:
            self.tester.keep_alive = keep_alive

        result = self.tester.run_api(
            api_config=json_to_be_tested["Logout"],
            api_name="Logout",
            override_headers={
                "Authorization": "Bearer " + str(GlobalAPIVariable.FubonAppResult["access_token"]),
                "accept": "text/plain"
            }
        )
        print(f"Logout 結果: {result}")
        print(f"Logout Response Text: ", self.tester.last_response_text)