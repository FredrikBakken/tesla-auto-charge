#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.sql import and_
from sqlalchemy.orm import sessionmaker

from models import Base, ElectricalPrices_TemporaryStorage


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
    else:
        print(location + ' ' + date + ' ' + hour + ' ' + price + ' already exist.')


### SELECT: Presentation for elspot site
def select_location_elspot(location):
    s = session()

    s_result = s.query(ElectricalPrices_TemporaryStorage).filter(ElectricalPrices_TemporaryStorage.location.like(location))

    location = ''
    date = ''
    values = []
    results = []

    for row in s_result:
        location = row.location
        date = row.date
        values.append(row.price)
        result = [row.hour, row.price]
        results.append(result)

    return location, date, values, results


### DELETE: Delete ElectricalPrices_TemporaryStorage entries no longer needed
def delete_old_elspot_temp(date, hour):
    s = session()

    d_result = s.query(ElectricalPrices_TemporaryStorage).filter((and_(ElectricalPrices_TemporaryStorage.date.like(date), ElectricalPrices_TemporaryStorage.hour.like(hour)))).delete(synchronize_session=False)
    s.commit()
