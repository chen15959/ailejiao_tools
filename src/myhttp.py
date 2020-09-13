# 封装HTTP(S)请求

import requests
import threading
import json

# 业务服务器
APP_SERVER = "https://api2.easyteaching.cn"



# 管理自定义HTTP头
class Header(object):
    _instance_lock = threading.Lock()
    _token = ""

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Header, "_instance"):
            with Header._instance_lock:
                if not hasattr(Header, "_instance"):
                    Header._instance = object.__new__(cls)

        return Header._instance


    def set_token(self, token):
        self._token = token;

    def get_login_header(self):
        return {"appid" : "easyteaching_app", "Content-Type" : "application/x-www-form-urlencoded"}

    def get_normal_header(self):
        return {"appid" : "easyteaching_app", "token" : self._token}





# 用户登录 获得token
def login(phone, password):
    form = "password=%s&phone=%s&platform=app" % (password, phone)
    r = requests.post(url = APP_SERVER + "/token/login", data = form, headers = Header().get_login_header(), verify = False)
    if (r.status_code == 200):
        jr = json.loads(r.text)
        if (jr["success"] == True):
            Header().set_token(jr["data"]["token"])
            return True

    print("LOGIN FAILED.")
    return False



def get(url):
    r = requests.get(url = url, headers = Header().get_normal_header(), verify = False)
    if (r.status_code == 200):
        jr = r.json()
        if (jr["success"] == True):
            return jr["data"]

    print("FAILED.")
    return False


def download(url, filename):
    r = requests.get(url = url, headers = Header().get_normal_header(), verify = False)
    if (r.status_code == 200):
        f = open(filename, "wb")
        f.write(r.content)
        f.close()
        return True
    else:
        return False







if __name__ == "__main__":
    login('*','*')



