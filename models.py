from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id              = Column(Integer, primary_key=True)
    elspot_location = Column(String)
    

class ElectricalPrices_TemporaryStorage(Base):
    __tablename__ = 'elprices_temp'

    id          = Column(Integer, primary_key=True)
    location    = Column(String)
    date        = Column(String(10))
    hour        = Column(String(13))
    price       = Column(String)


class HistoricStorage(Base):
    __tablename__ = 'historic_storage'

    id          = Column(Integer, primary_key=True)
    # MORE
