#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import binascii
import json


### Used for setting up a secure key to avoid csrf-attacks
def set_secret_key():
    key = os.urandom(24)
    return key


### Check if authentication settings are set
def check_authentication():
    result = ['False', 'False', 'False']
    jdata = json.loads(open('config.json').read())
    username = jdata['settings-authentication']['username']
    password = jdata['settings-authentication']['password']

    if username != "admin" and password != "qwerty":
        result[0] = "set_auth"
    if username != "admin":
        result[1] = "set_username"
    if password != "qwerty":
        result[2] = "set_password"
    
    return result


### Get username and password from config
def get_basic_authentication():
    jdata = json.loads(open('config.json').read())
    basic_auth_username = jdata['settings-authentication']['username']
    basic_auth_password = jdata['settings-authentication']['password']
    return basic_auth_username, basic_auth_password


### Set new basic authentication username
def set_new_authentication_username(app, new_username):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['settings-authentication']['username'] = new_username
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    # Activate new username to current session
    app.config['BASIC_AUTH_USERNAME'] = new_username


### Set new basic authentication password
def set_new_authentication_password(app, new_password):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['settings-authentication']['password'] = new_password
        f.seek(0)
        json.dump(data, f)
        f.truncate()

    # Activate new password to current session
    app.config['BASIC_AUTH_PASSWORD'] = new_password


### Check if location is set
def check_location():
    result = ['False']
    jdata = json.loads(open('config.json').read())
    current_location = jdata['elspot-settings']['home-location']

    if current_location != "":
        result[0] = 'set_location'
    
    return result


### Get current elspot location
def get_current_elspot_location():
    jdata = json.loads(open('config.json').read())
    current_location = jdata['elspot-settings']['home-location']
    return current_location


### Set new elspot location
def set_new_elspot_location(new_location):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['elspot-settings']['home-location'] = new_location
        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Set if vehicle settings are set
def check_vehicle():
    result = ['False', 'False', 'False']
    jdata = json.loads(open('config.json').read())

    username        = jdata['vehicle-settings']['username']
    password        = jdata['vehicle-settings']['password']

    latitude        = jdata['vehicle-settings']['home-latitude']
    longitude       = jdata['vehicle-settings']['home-longitude']

    if username != "" and password != "":
        result[1] = "set_auth"
    
    if latitude != "" and longitude != "":
        result[2] = "set_location"

    if result[1] != 'False' and result[2] != 'False':
        result[0] = "set_vehicle"
    
    return result


### Set vehicle authentication
def set_vehicle_authentication(username, password):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['vehicle-settings']['username'] = username
        data['vehicle-settings']['password'] = password
        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Set vehicle current location
def set_vehicle_current_location(latitude, longitude):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['vehicle-settings']['current-latitude'] = latitude
        data['vehicle-settings']['current-longitude'] = longitude
        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Set vehicle home location
def set_vehicle_home_location(latitude, longitude):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['vehicle-settings']['home-latitude'] = latitude
        data['vehicle-settings']['home-longitude'] = longitude
        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Get vehicle's home location
def get_vehicle_home_location():
    jdata = json.loads(open('config.json').read())
    latitude = jdata['vehicle-settings']['home-latitude']
    longitude = jdata['vehicle-settings']['home-longitude']
    return latitude, longitude


### Set charge vehicle to settings
def set_charge_to(to_date, to_time):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data['charge-timer']['to-date'] = to_date
        data['charge-timer']['to-time'] = to_time
        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Get charge to settings
def get_charge_to():
    jdata = json.loads(open('config.json').read())
    to_date = jdata['charge-timer']['to-date']
    to_time = jdata['charge-timer']['to-time']
    return to_date, to_time


### Adding charge schedule to json
def set_charge_schedule(charge_schedule):
    with open('config.json', 'r+') as f:
        data = json.load(f)

        data['charge-schedule'] = []

        for x in range(len(charge_schedule)):
            data['charge-schedule'].insert(x, {'date': charge_schedule[x][0], 'hour': charge_schedule[x][1], 'price': charge_schedule[x][2], 'min': charge_schedule[x][3]})

        f.seek(0)
        json.dump(data, f)
        f.truncate()


### Get charge schedule
def get_charge_schedule():
    jdata = json.loads(open('config.json').read())
    charge_schedule = jdata['charge-schedule']
    return charge_schedule
