#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from datetime import datetime, timedelta
from dateutil.tz import *

# Import libraries for fetching elspot data from Nordpoolspot
from nordpool import elspot
from pprint import pprint

from database import insert_all_elspot


# Fetch hourly spot prices
def get_spot_values():
    exist = True
    prices_spot_hourly = elspot.Prices().hourly()
    locations = ['SE1', 'SE2', 'SE3', 'SE4', 'FI', 'DK1', 'DK2', 'Oslo', 'Kr.sand', 'Bergen', 'Molde', 'Tr.heim', 'Tromsø', 'EE', 'LV', 'LT']

    for x in range(len(locations)):
        location = locations[x]

        # Find local time offset
        local_time = datetime.now(tzlocal()).strftime("%H")
        global_utc = datetime.now(tzlocal()).astimezone(tzoffset(None, 0)).strftime("%H")
        offset = int(local_time) - int(global_utc)

        # Getting the elspot date
        spot_date = prices_spot_hourly.get('areas', {}).get(location, {}).get('values')[12].get('start').strftime("%Y.%m.%d")

        # Store hourly price results
        if not prices_spot_hourly.get('areas', {}).get(location, {}).get('values')[0].get('value') == float('inf'):
            for y in range(24):
                spot_time       = prices_spot_hourly.get('areas', {}).get(location, {}).get('values')[y].get('start')
                spot_from       = spot_time + timedelta(hours=offset)
                spot_to         = spot_time + timedelta(hours=offset+1)
                spot_timeframe  = spot_from.strftime("%H:%M") + ' - ' + spot_to.strftime("%H:%M")
                spot_value      = "%.2f" % prices_spot_hourly.get('areas', {}).get(location, {}).get('values')[y].get('value')

                exist = insert_all_elspot(location, spot_date, spot_timeframe, spot_value)

    return exist
