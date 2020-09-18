# 封装HTTP(S)请求

import requests
import threading
import json

#from config import Config
from config import load_config, is_ready, set_token, get_login_header, get_normal_header, get_user, get_password


# 业务服务器
APP_SERVER = "https://api2.easyteaching.cn"



# 管理自定义HTTP头
# class Header(object):
#     _instance_lock = threading.Lock()
#     _token = ""
#
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Header, "_instance"):
#             with Header._instance_lock:
#                 if not hasattr(Header, "_instance"):
#                     Header._instance = object.__new__(cls)
#
#         return Header._instance
#
#
#     def set_token(self, token):
#         self._token = token
#
#     def get_login_header(self):
#         return {"appid" : "easyteaching_app", "Content-Type" : "application/x-www-form-urlencoded"}
#
#     def get_normal_header(self):
#         return {"appid" : "easyteaching_app", "token" : self._token}
#
#
def get_data(response):
    if response.status_code == 200:
        jr = json.loads(response.text)
        if jr['success'] == True:
            return jr['data']

    raise Exception


# 用户登录 获得token
def login():
    form = "password=%s&phone=%s&platform=app" % (get_password(), get_user())
    r = requests.post(url = APP_SERVER + "/token/login", data = form, headers = get_login_header(), verify = False)
    jr = get_data(r)
    set_token(jr['token'])


def verify():
    try:
        get(APP_SERVER + "/token/work_count?platform=app")
    except:
        set_token('')



def get(url):
    r = requests.get(url = url, headers = get_normal_header(), verify = False)
    return get_data(r)



def download(url, filename):
    r = requests.get(url = url, headers = get_normal_header(), verify = False)
    if (r.status_code == 200):
        f = open(filename, "wb")
        f.write(r.content)
        f.close()
        return True
    else:
        return False


def prepare():
    load_config('config.ini')

    while not is_ready():
        try:
            login()
        except:
            pass

    verify()

    return is_ready()







if __name__ == "__main__":
    prepare()




