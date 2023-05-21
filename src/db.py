from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VIN_Cache(Base):
    __tablename__ = 'vin_cache'

    vin = Column(String, primary_key=True)
    make = Column(String)
    model = Column(String)
    year = Column(String)
    body_class = Column(String)
