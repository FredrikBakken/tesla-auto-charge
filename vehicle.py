#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import json
import logging
import teslajson

from datetime import datetime
from threading import Timer

from config import set_vehicle_authentication, set_vehicle_current_location, get_vehicle_home_location


# Register vehicle credentials
def register_credentials(username, password):
    try:
        connection = teslajson.Connection(username, password)
        set_vehicle_authentication(username, password)
        return True
    except:
        return False


# Connect to the vehicle
def vehicle_connection():
    jdata = json.loads(open('config.json').read())
    vehicle_username = jdata['vehicle-settings']['username']
    vehicle_password = jdata['vehicle-settings']['password']

    try:
        connection = teslajson.Connection(vehicle_username, vehicle_password)
        return connection
    except:
        return False


# Get vehicle's current location (if home location is not set)
def get_vehicle_current_location():
    jdata = json.loads(open('config.json').read())
    home_latitude = jdata['vehicle-settings']['home-latitude']
    home_longitude = jdata['vehicle-settings']['home-longitude']

    if home_latitude == "" and home_longitude == "":
        connection = vehicle_connection()

        if connection:
            vehicle = connection.vehicles[0]
            result = vehicle.data_request('drive_state')

            lat = result['latitude']
            lng = result['longitude']

            set_vehicle_current_location(lat, lng)


# Vehicle location settings page
def vehicle_location():
    lat = ""
    lng = ""
    zoom = ""
    add_marker = ""

    jdata = json.loads(open('config.json').read())
    home_latitude = jdata['vehicle-settings']['home-latitude']
    home_longitude = jdata['vehicle-settings']['home-longitude']
    current_latitude = jdata['vehicle-settings']['current-latitude']
    current_longitude = jdata['vehicle-settings']['current-longitude']

    if (home_latitude != "" and home_longitude != ""):
        lat = home_latitude
        lng = home_longitude
        zoom = 15
        add_marker = "y"
    elif (current_latitude != "" and current_longitude != ""):
        lat = current_latitude
        lng = current_longitude
        zoom = 10
        add_marker = "n"
    else:
        lat = 57.665522
        lng = 11.164774
        zoom = 4
        add_marker = "n"

    return lat, lng, zoom, add_marker


# Start car charging
def start_charge(vehicle):
    command = vehicle.command('charge_start')
    response = command['result']

    if response:
        return True
    else:
        return False


# Stop car charging
def stop_charge(vehicle):
    command = vehicle.command('charge_stop')
    response = command['result']

    if response:
        return True
    else:
        return False


# Scheduled charge stop
def scheduled_stop_charge(time_hour, time_minutes):
    today = datetime.today()
    stop_timer = today.replace(day=today.day, hour=int(time_hour[:2]), minute=int(time_minutes), second=0, microsecond=0)
    delta_t = stop_timer - today

    secs = delta_t.seconds + 1

    def schedule_stopper():
        # TODO
        #connection = vehicle_connection()
        #vehicle = connection.vehicles[0]
        #stop_charge(vehicle)
        print('Charging force stopped at ' + stop_timer.strftime("%Y.%m.%d %H:%M"))
        logging.info('Vehicle charging force stopped at ' + stop_timer.strftime("%Y.%m.%d %H:%M") + '.')

    t = Timer(secs, schedule_stopper)
    t.start()
