# 封装HTTP(S)请求

import requests
import threading
import json
import urllib3

from config import Config



# 业务服务器
APP_SERVER = "https://api2.easyteaching.cn"




def get_data(response):
    if response.status_code == 200:
        jr = json.loads(response.text)
        if jr['success'] == True:
            return jr['data']

    raise Exception


# 用户登录 获得token
def login():
    form = "password=%s&phone=%s&platform=app" % (Config().get('password'), Config().get('user'))
    r = requests.post(url = APP_SERVER + "/token/login", data = form, headers = {"appid" : "easyteaching_app", "Content-Type" : "application/x-www-form-urlencoded"}, verify = False)
    jr = get_data(r)
    Config().set_token(jr['token'])
    Config().set_user(jr['id'])



def verify():
    try:
        get(APP_SERVER + "/token/work_count?platform=app")
        return True
    except:
        Config().set_token('')
        return False



def get(url):
    for i in range(1,5):
        try:
            r = requests.get(url = url, headers = Config().get_header(), verify = False, timeout=30)
            return get_data(r)
        except requests.exceptions.ConnectTimeout:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.Timeout:
            pass

    raise requests.exceptions.Timeout



def post(url, data):
    for i in range(1,5):
        try:
            r = requests.post(url = url, data = data, headers = Config().get_header(), verify = False, timeout=30)
            return get_data(r)
        except requests.exceptions.ConnectTimeout:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.Timeout:
            pass

    raise requests.exceptions.Timeout


def download(url, filename):
    for i in range(1,5):
        try:
            r = requests.get(url = url, headers = Config().get_header(), verify = False, timeout=30)
            if (r.status_code == 200):
                f = open(filename, "wb")
                f.write(r.content)
                f.close()
                return True
            else:
                return False
        except requests.exceptions.ConnectTimeout:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.Timeout:
            pass

    raise requests.exceptions.Timeout


def prepare():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    Config().load('config.ini')

    if Config().is_ready():
        if verify():
            return True


    for i in range(1, 5):
        try:
            login()
            break
        except:
            if i > 5:
                break




    if verify():
        Config().save('config.ini')
        return True
    else:
        return False







if __name__ == "__main__":
    print(prepare())




