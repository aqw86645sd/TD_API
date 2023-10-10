import json


class class_static_param:
    def __init__(self):
        self.file_1_td_config = "file_1_td_config.json"
        self.file_2_td_code = "file_2_td_code.json"
        self.file_3_td_token = "file_3_td_token.json"
        self.file_4_line_token = "file_4_line_token"

        with open(self.file_1_td_config, "r") as f:
            data_str = f.read()
            data_json = json.loads(data_str)

        self.code_replace_str = data_json["Callback URL"] + "/?code="

        self.td_auth_url = "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={}&client_id={}@AMER.OAUTHAP"

        self.td_api_accounts = "https://api.tdameritrade.com/v1/accounts?fields=positions"
