import configparser
import threading



global myconfig;


def load_config(file_name):
    global myconfig
    myconfig = configparser.ConfigParser()
    myconfig.read(file_name)


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



