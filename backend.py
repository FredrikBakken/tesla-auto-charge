#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import schedule

from dateutil.tz import *
from threading import Thread
from datetime import datetime

from config import get_charge_to
from charger import charge_ready, configure_charge, charge_scheduler, run_charging
from vehicle import get_vehicle_current_location
from spot_values import get_spot_values


charge_test = True
vehicle_ready = False


# Scheduled vehicle charger
def vehicle_charge_scheduler():
    global charge_test
    global vehicle_ready

    vehicle_ready = charge_ready()
    print(vehicle_ready)

    if vehicle_ready:
        if charge_test:
            configure_charge()
            charge_scheduler()
            charge_test = False
    else:
        charge_test = True
        vehicle_ready = False


# Vehicle charger
def vehicle_charger():
    if not charge_test:
        run_charging()
    else:
        vehicle_charge_scheduler()


# Schedule getting newest elspot data
def elspot_handler():
    exist = get_spot_values()

    to_date = get_charge_to()[0]
    to_date = datetime.strptime(to_date, "%Y.%m.%d")
    now = datetime.now()

    if not exist and to_date > now:
        charge_test = True


def run_schedule():
    # TODO: Do this once at initialization
    #get_spot_values()
    #get_vehicle_current_location()

    while 1:
        schedule.run_pending()
        time.sleep(1)


def scheduler():
    # Execute the elspot data updater
    # schedule.every().hour.at(':45').do(elspot_handler)

    # Execute the vehicle charge scheduler
    schedule.every(2).minutes.do(vehicle_charge_scheduler)
    
    # Execute the vehicle charging every hour
    schedule.every().hour.at(':08').do(vehicle_charger)

    # Schedule logging to database about previous hour actions (perform this action every hour at :05, or at the same time as the vehicle_charger is ran)
    # TODO
    
    # Start threading
    t = Thread(target=run_schedule)
    t.start()
