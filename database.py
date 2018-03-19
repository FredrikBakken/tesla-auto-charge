#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pytz
import datetime

from sqlalchemy import create_engine
from sqlalchemy.sql import and_
from sqlalchemy.orm import sessionmaker

from models import Base, ElectricalPrices_TemporaryStorage, PreviousCharges


# Initialize the engine
engine = create_engine('sqlite:///db/tac_db.db', echo=True)

# Initialize and configure the session
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


### INSERT: Elspot
def insert_all_elspot(location, date, hour, price):
    s = session()

    exist = False
    s_result = s.query(ElectricalPrices_TemporaryStorage).filter(and_(ElectricalPrices_TemporaryStorage.location.like(location), ElectricalPrices_TemporaryStorage.date.like(date), ElectricalPrices_TemporaryStorage.hour.like(hour), ElectricalPrices_TemporaryStorage.price.like(price)))

    for row in s_result:
        exist = True

    if not exist:    
        new_spot = ElectricalPrices_TemporaryStorage(location=location, date=date, hour=hour, price=price)
        s.add(new_spot)
        s.commit()
    
    delete_old_elspot_temp()

    return exist


### SELECT: Presentation for elspot site
def select_location_elspot(location):
    s = session()

    s_result = s.query(ElectricalPrices_TemporaryStorage).filter(ElectricalPrices_TemporaryStorage.location.like(location)).order_by(ElectricalPrices_TemporaryStorage.date.asc()).order_by(ElectricalPrices_TemporaryStorage.hour.asc())

    from_date = ''
    to_date   = ''
    labels    = []
    values    = []
    results   = []

    from_date = s_result[0].date
    to_date = s_result[-1].date
    dates = from_date + ' - ' + to_date

    for row in s_result:
        label_hour = row.hour[:5]
        label_time = time.strptime(label_hour, "%H:%M")
        label_integer = str(label_time.tm_hour)
        labels.append(label_integer)

        values.append(row.price)
        result = [row.date, row.hour, row.price]
        results.append(result)

    return location, dates, labels, values, results


### DELETE: Delete ElectricalPrices_TemporaryStorage entries no longer needed
def delete_old_elspot_temp():
    s = session()

    # Find dates stored in temp database
    dates = []
    q_all_dates = s.query(ElectricalPrices_TemporaryStorage).order_by(ElectricalPrices_TemporaryStorage.date.asc())

    for row in q_all_dates:
        if not row.date in dates:
            dates.append(row.date)

    now = datetime.datetime.now().strftime("%Y.%m.%d")
    today = datetime.datetime.strptime(now, "%Y.%m.%d")

    # Go through dates in temporary database
    for x in range(len(dates)):
        check_date = datetime.datetime.strptime(dates[x], "%Y.%m.%d")

        if today > check_date:
            delete_date = check_date.strftime("%Y.%m.%d")

            q_delete_entries = s.query(ElectricalPrices_TemporaryStorage).filter(ElectricalPrices_TemporaryStorage.date == delete_date).delete()
            s.commit()
