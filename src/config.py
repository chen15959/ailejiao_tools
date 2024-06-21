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
                if not line.startswith('#'):
                    parts = line.rstrip('\n').split('=', maxsplit=1)
                    if len(parts) == 2:
                        self.data[parts[0].strip(' ')] = parts[1].strip(' ')

    def save(self, filename):
        with open(filename, 'w') as fp:
            for k in iter(self.data):
                fp.write("%s=%s\n" % (k, self.data[k]))


    def get(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return ''


    def is_ready(self):
        return self.get('token') != ''


    def set_token(self, token):
        self.data['token'] = token

    def set_user(self, userid):
        self.data['userid'] = userid


    def get_header(self):
        return {"appid": "easyteaching_ios", "token": self.get('token'), "BuildVersion": "326"}


    def debug(self):
        return True



