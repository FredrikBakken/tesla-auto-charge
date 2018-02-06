import os
import binascii
import json


### Used for setting up a secure key to avoid csrf-attacks
def set_secret_key():
    key = os.urandom(24)
    return key


### Get username and password from config
def get_basic_authentication():
    jdata = json.loads(open('config.json').read())
    basic_auth_username = jdata['settings-authentication']['username']
    basic_auth_password = jdata['settings-authentication']['password']

    return basic_auth_username, basic_auth_password


### Set new password
def set_new_authentication_password(new_password):
    return True
