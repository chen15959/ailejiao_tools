import configparser
import threading



class Config(object):
    _instance_lock = threading.Lock()
    data = {}


    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = object.__new__(cls)

        return Config._instance


    def __init__(self):
        pass


    def load(self, filename):
        with open(filename, 'r') as fp:
            for line in fp.readlines():
                parts = line.rstrip('\n').split('=', maxsplit=1)
                if len(parts) == 2:
                    self.data[parts[0].strip(' ')] = parts[1].strip(' ')

    def save(self, filename):
        with open(filename, 'w') as fp:
            for k in iter(self.data):
                fp.write("%s=%s\n" % (k, self.data[k]))


    def get(self, key):
        return self.data[key]


    def is_ready(self):
        return self.data['token'] != ''


    def set_token(self, token):
        self.data['token'] = token


    def get_header(self):
        return {"appid": "easyteaching_app", "token": self.get('token')}




global myconfig;


def load_config(file_name):
    global myconfig
    myconfig = configparser.ConfigParser()
    myconfig.read(file_name)

def save_config(filename):
    global myconfig
    with open(filename, 'w') as fp:
        myconfig.write(fp)


def is_ready():
    global myconfig
    return myconfig['login']['token'] != ''


def set_token(token):
    global myconfig
    myconfig['login']['token'] = token


def get_login_header():
    return {"appid" : "easyteaching_app", "Content-Type" : "application/x-www-form-urlencoded"}


def get_normal_header():
    global myconfig
    return {"appid" : "easyteaching_app", "token" : myconfig['login']['token']}


def get_user():
    global myconfig
    return myconfig['login']['user']

def get_password():
    global myconfig
    return myconfig['login']['password']

def get_download_folder():
    global myconfig
    return myconfig['download']['folder']
