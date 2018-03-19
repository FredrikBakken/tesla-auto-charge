#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time

from pprint import pprint

from dateutil.tz import *
from datetime import datetime, timedelta

from backend import vehicle_charger
from spot_values import get_spot_values
from database import insert_all_elspot, delete_old_elspot_temp, select_location_elspot, delete_old_elspot_temp
from config import set_secret_key, check_authentication, check_location, get_vehicle_home_location, get_charge_schedule
from vehicle import vehicle_connection, scheduled_stop_charge
from charger import charge_scheduler, run_charging


# Used to perform manual tests without running the Flask site

def run():
    get_spot_values()

    return True

# Define startup functionality
if __name__ == "__main__":
    run()