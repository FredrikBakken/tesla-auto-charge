#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from dateutil.tz import *

# Import libraries for fetching elspot data from Nordpoolspot
from nordpool import elspot
from pprint import pprint

from database import insert_all_elspot


# Fetch hourly spot prices
def get_spot_values():
    prices_spot_hourly = elspot.Prices().hourly()

    for x in range(len(prices_spot_hourly['areas'])):
        # Find local time offset
        local_time = datetime.now(tzlocal()).strftime("%H")
        global_utc = datetime.now(tzlocal()).astimezone(tzoffset(None, 0)).strftime("%H")
        offset = int(local_time) - int(global_utc)

        # Getting the elspot date
        spot_date = prices_spot_hourly['areas'][x]['values'][12]['start'].strftime("%Y-%m-%d")  # Can this cause issues for the correct date?

        # Store hourly price results
        if not prices_spot_hourly['areas'][x]['values'][0]['value'] == float('inf'):
            for y in range(24):
                spot_time       = prices_spot_hourly['areas'][x]['values'][y]['start']
                spot_from       = spot_time + timedelta(hours=offset)
                spot_to         = spot_time + timedelta(hours=offset+1)
                spot_timeframe  = spot_from.strftime("%H:%M") + ' - ' + spot_to.strftime("%H:%M")
                spot_value      = "%.2f" % prices_spot_hourly['areas'][x]['values'][y]['value']

                insert_all_elspot(x, spot_date, spot_timeframe, spot_value)
