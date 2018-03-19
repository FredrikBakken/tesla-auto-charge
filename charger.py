#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import math
import json
import logging

from threading import Timer
from datetime import datetime, timedelta

from config import get_current_elspot_location, get_charge_to, set_charge_schedule, get_charge_schedule
from vehicle import vehicle_connection, scheduled_stop_charge
from database import select_location_elspot


measure_time = 0
battery_level = 0
charger_current = 0
charger_voltage = 0
time_to_full_charge = 0     # TODO: 0
minutes_to_full_charge = 0  # TODO: 0


# Check if vehicle is in defined home location and is ready to charge
def charge_ready():
    connection = vehicle_connection()

    in_range = False
    in_charge = False

    if connection:
        vehicle = connection.vehicles[0]
        '''
        # Check if vehicle is in range of home location
        current_position = vehicle.data_request('drive_state')
        current_lat = current_position['latitude']
        current_lng = current_position['longitude']

        home_position = get_vehicle_home_location()
        home_lat = home_position[0]
        home_lng = home_position[1]

        if current_lat >= (float(home_lat) - 0.005) and current_lat <= (float(home_lat) + 0.005):
            if current_lng >= (float(home_lng) - 0.005) and current_lng <= (float(home_lng) + 0.005):
                in_range = True
        '''
        in_range = True     # TODO: REMOVE
        time.sleep(5)

        # Confirm vehicle charge state
        '''
        charge_state = vehicle.data_request('charge_state')
        charge_port_door_open = charge_state['charge_port_door_open']
        charge_port_latch = charge_state['charge_port_latch']

        if charge_port_door_open and charge_port_latch == 'Engaged':
            in_charge = True
        '''
        in_charge = True    # TODO: REMOVE
        
        if in_range and in_charge:
            return True
        else:
            return False
    else:
        return False


# Configure the charge schedule
def configure_charge():
    start_issues = True
    stop_issues  = True

    # Setup vehicle connection
    connection = vehicle_connection()
    vehicle = connection.vehicles[0]

    while (start_issues or stop_issues):
        # Start charging
        #start_response = start_charge(vehicle)
        start_response = True   # TODO: REMOVE

        # Check for response issues
        if start_response:
            start_issues = False
        
        # Charge for 5min
        time.sleep(3)

        # Get the current charge state for the vehicle
        # charge_state = vehicle.data_request('charge_state') TODO

        global measure_time
        global battery_level
        global charger_current
        global charger_voltage
        global time_to_full_charge
        global minutes_to_full_charge

        # TODO: HANDLE THE RESPONSE FROM THE VEHICLE
        #state_response = vehicle.data_request('charge_state')
        measure_time = datetime.now().strftime("%Y.%m.%d %H:%M")
        battery_level = 75 #state_response['battery_level']
        charger_current = 13 #state_response['charger_actual_current']
        charger_voltage = 234 #state_response['charger_voltage']
        time_to_full_charge = 5.65 #state_response['time_to_full_charge']
        minutes_to_full_charge = 40 #math.ceil((state_response['time_to_full_charge'] - math.floor(state_response['time_to_full_charge'])) * 60)

        # Sleep before next command
        time.sleep(5)

        # Stop charging
        #stop_response = stop_charge(vehicle)
        stop_response = True    # TODO: REMOVE

        # Check for response issues
        if stop_response:
            stop_issues = False
    
    return True


# Charge scheduler
def charge_scheduler():
    # Prices and times from database
    location = get_current_elspot_location()
    unformatted_result = select_location_elspot(location)[4]

    # From time
    datetime_now = datetime.now()
    from_date = datetime_now.strftime("%Y.%m.%d")
    from_time = datetime_now

    if from_time.strftime("%M") == '00':
        from_time = from_time.strftime("%H")
    else:
        from_time = (from_time + timedelta(hours=1)).strftime("%H")

    charge_to = get_charge_to()
    to_date = charge_to[0]
    to_time = charge_to[1]
    
    if (to_date == unformatted_result[0][0] or to_date == unformatted_result[-1][0]) and from_time < to_time[:2]:
        to_date = to_date
        to_time = to_time
    else:
        to_date = unformatted_result[-1][0]
        to_time = '00:00'

    charge_times = []

    bool_time_from = False
    bool_time_to = False

    for x in range(len(unformatted_result)):
        list_time = unformatted_result[x][1]
        list_time = list_time[8:10]

        if (from_date == unformatted_result[x][0] and list_time == from_time[:2]):
            bool_time_from = True

        if bool_time_to is False and bool_time_from:
            charge_times.append(unformatted_result[x])

        if (to_date == unformatted_result[x][0] and list_time == to_time[:2]):
            bool_time_to = True

    charge_times_sorted = sorted(charge_times, key=lambda x : x[2])[:math.ceil(time_to_full_charge)]

    for x in range(len(charge_times_sorted) - 1):
        charge_times_sorted[x].append('60')

    charge_times_sorted[-1].append(str(minutes_to_full_charge))

    set_charge_schedule(charge_times_sorted)


# Running the actual charging
def run_charging():
    datetime_now = datetime.now()
    datetime_now_ahead = datetime_now + timedelta(hours=1)
    
    date = datetime_now.strftime("%Y.%m.%d")
    hour = datetime_now.strftime("%H") + ':00 - ' + datetime_now_ahead.strftime("%H") + ':00'

    charge_schedule = get_charge_schedule()

    # TODO
    #connection = vehicle_connection()
    #vehicle = connection.vehicles[0]

    if (any(d['date'] == date for d in charge_schedule) and any(h['hour'] == hour for h in charge_schedule)):
        print('CHARGE STARTING AT ' + hour)
        logging.info('Vehicle charging starting ' + hour + '.')
        #stop_charge(vehicle)   # TODO
    else:
        print('CHARGE STOPPING AT ' + hour)
        logging.info('Vehicle charging stopping at ' + hour + '.')
        #start_charge(vehicle)  # TODO
    
    maxPricedItem = max(charge_schedule, key=lambda x:x['price'])

    if hour == maxPricedItem['hour']:
        scheduled_stop_charge(hour, minutes_to_full_charge)
