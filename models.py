#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ElectricalPrices_TemporaryStorage(Base):
    __tablename__ = 'elprices_temp'

    id          = Column(Integer, primary_key=True)
    location    = Column(String)
    date        = Column(String(10))
    hour        = Column(String(13))
    price       = Column(String)


class PreviousCharges(Base):
    __tablename__ = 'previous_charges'

    id          = Column(Integer, primary_key=True)
    location    = Column(String)
    date        = Column(String(10))
    hour        = Column(String(13))
    price       = Column(String)
    #bat_lvl     = Column(String(3))
    #charge_start= Column(String(5)) # Information about charge start only at charge_from
    #charge_stop = Column(String(5)) # At exact which time charging stops

    # ...
