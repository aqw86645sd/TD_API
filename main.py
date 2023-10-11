import requests
import os
import json
import pygsheets
from urllib.parse import unquote


class Entrance:
    def __init__(self):
        # file
        self.file_google_sheet_url = "file_google_sheet_url"
        self.file_google_sheet_json = "file_td_api_config_pygsheet.json"

        # url
        self.td_auth_url = "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={}&client_id={}@AMER.OAUTHAP"
        self.td_api_accounts = "https://api.tdameritrade.com/v1/accounts?fields=positions"

        # class
        self.gc = None
        self.sht = None

        # google sheet info
        self.wks_td_api_page = 0  # 頁 index
        self.consumer_key_cell = "B1"
        self.callback_url_cell = "B2"
        self.wks_td_code_page = 1  # 頁 index
        self.code_cell = "B1"
        self.decode_cell = "B2"
        self.wks_td_token_page = 2  # 頁 index
        self.access_token_cell = "B1"
        self.refresh_token_cell = "B2"
        self.scope_cell = "B3"
        self.expires_in_cell = "B4"
        self.refresh_token_expires_in_cell = "B5"
        self.token_type_cell = "B6"
        self.wks_line_token_page = 3  # 頁 index
        self.line_token_cell = "A1"

        # variable
        self.google_sheet_url = ""
        self.consumer_key = ""
        self.callback_url = ""
        self.code = ""
        self.decode = ""
        self.access_token = ""
        self.refresh_token = ""
        self.scope = ""
        self.expires_in = ""
        self.refresh_token_expires_in = ""
        self.token_type = ""
        self.line_token = ""

    def run(self):
        # check file
        if not os.path.exists(self.file_google_sheet_url):
            with open(self.file_google_sheet_url, "w") as file:
                file.write("")

        with open(self.file_google_sheet_url, "r") as f:
            self.google_sheet_url = f.read()

        if len(self.google_sheet_url) == 0:
            print("清輸入 file_google_sheet_url 內容！")
            quit()

        self.fn_get_sheet_info()

        # 先打 requests 確認
        auth_ = "Bearer " + self.access_token

        headers = {
            "Authorization": auth_
        }

        req = requests.get(self.td_api_accounts, headers=headers)

        if req.status_code != 200:
            self.fn_line_notify_message("TD API token 過期！！")

            # todo 更新

            print(self.fn_get_td_auth_url())

            print(self.fn_decode_code())
            quit()

        req_json = req.json()

        positions_list = req_json[0]["securitiesAccount"]["positions"]

        for ticker_data in positions_list:
            print(ticker_data["instrument"]["symbol"])

        a = self.td_auth_url.format(self.callback_url, self.consumer_key)

        self.fn_line_notify_message('test:' + a)

    def fn_get_sheet_info(self):
        # connect google sheet
        self.gc = pygsheets.authorize(service_file=self.file_google_sheet_json)
        self.sht = self.gc.open_by_url(self.google_sheet_url)

        # td api
        wks = self.sht[self.wks_td_api_page]
        self.consumer_key = wks.cell(self.consumer_key_cell).value
        self.callback_url = wks.cell(self.callback_url_cell).value

        # code
        wks = self.sht[self.wks_td_code_page]
        self.code = wks.cell(self.code_cell).value
        self.decode = wks.cell(self.decode_cell).value

        # td token

        # line token
        wks = self.sht[self.wks_line_token_page]
        self.line_token = wks.cell(self.line_token_cell).value

    def fn_get_td_auth_url(self):
        return self.td_auth_url.format(self.callback_url, self.consumer_key)

    def fn_decode_code(self):
        decode_str = unquote(self.code.replace(self.callback_url + "/?code=", ""))
        # code
        wks = self.sht[self.wks_td_code_page]
        wks.update_value(self.decode_cell, decode_str)
        return decode_str

    def fn_line_notify_message(self, msg):
        # 跟line申請權杖
        token = self.line_token

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
