from class_static_param import class_static_param  # 固定參數設定檔
import requests
import os
import json
from urllib.parse import unquote


class Entrance(class_static_param):
    def __int__(self):
        pass

    def run(self):
        if self.def_check_config_file() is False:
            # notify
            print("*** file not existed ***")

            self.line_notify_message("TD API 請輸入相關 config！！")

            quit()

        # 正片開始
        # 直接使用舊的執行
        # get token
        with open(self.file_3_td_token, "r") as f:
            data_str = f.read()
            data_json = json.loads(data_str)

            auth_ = "Bearer " + data_json["access_token"]

        headers = {
            "Authorization": auth_
        }

        req = requests.get(self.td_api_accounts, headers=headers)

        if req.status_code != 200:
            self.line_notify_message("TD API token 過期！！")

            quit()

        req_json = req.json()

        positions_list = req_json[0]["securitiesAccount"]["positions"]

        for ticker_data in positions_list:
            print(ticker_data["instrument"]["symbol"])

        # 失敗重新取得
        self.get_td_auth_url()

        self.decode_code()

    def def_check_config_file(self):
        p_existed = True  # file is exist

        """ file 1 """
        if not os.path.isfile(self.file_1_td_config):
            p_existed = False

            json_td_config = {
                "Consumer Key": "",
                "Callback URL": ""
            }

            with open(self.file_1_td_config, "w") as file:
                file.write(json.dumps(json_td_config))

        """ file 2 """
        if not os.path.isfile(self.file_2_td_code):
            p_existed = False

            json_td_code = {
                "Code": ""
            }

            with open(self.file_2_td_code, "w") as file:
                file.write(json.dumps(json_td_code))

        """ file 3 """
        if not os.path.isfile(self.file_3_td_token):
            p_existed = False

            json_td_token = {
                "access_token": "",
                "refresh_token": "",
                "scope": "",
                "expires_in": None,
                "refresh_token_expires_in": None,
                "token_type": ""
            }

            with open(self.file_3_td_token, "w") as file:
                file.write(json.dumps(json_td_token))

        """ file 4 """
        if not os.path.isfile(self.file_4_line_token):
            p_existed = False

            with open(self.file_4_line_token, "w") as file:
                file.write("line token")

        return p_existed

    def get_td_auth_url(self):
        with open(self.file_1_td_config, "r") as f:
            data_str = f.read()
            data_json = json.loads(data_str)

            print(self.td_auth_url.format(data_json["Callback URL"], data_json["Consumer Key"]))

    def decode_code(self):
        with open(self.file_2_td_code, "r") as f:
            data_str = f.read()
            data_json = json.loads(data_str)

            print(unquote(data_json["Code"].replace(self.code_replace_str, "")))

    def line_notify_message(self, msg):
        # 跟line申請權杖

        token = ""

        with open(self.file_4_line_token, "r") as f:
            token = f.read()

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
        return r.status_code


if __name__ == '__main__':
    execute = Entrance()
    execute.run()
