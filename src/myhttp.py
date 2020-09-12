# 封装HTTP(S)请求

import requests
import json

# 业务服务器
APP_SERVER = "https://api2.easyteaching.cn"

# 权限令牌
TOKEN = ""

def get_headers():
    r = {
        "appid" : "easyteaching_app",

    }

def login(phone, password):
    form = "password=%s&phone=%s&platform=app" % (password, phone)
    r = requests.post(url = APP_SERVER + "/token/login", data = form, headers = {"appid" : "easyteaching_app", "Content-Type" : "application/x-www-form-urlencoded"}, verify = False)
    if (r.status_code == 200):
        jr = json.loads(r.text)
        if (jr["success"] == True):
            TOKEN = jr["data"]["token"]
            return True

    print("LOGIN FAILED.")
    return False





if __name__ == "__main__":
    login('*','*')
    print("here")


