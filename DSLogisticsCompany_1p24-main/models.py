from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    orderID = Column(Integer, primary_key=True, index=True)
    Product = Column(String, index=True)
    orderState = Column(String, index=True)
    deliveryDate = Column(Date)
    destinationLocation = Column(String)
    statimatedDeliveryTime = Column(Time)

class Fleet(Base):
    __tablename__ = "fleets"

    fleetID = Column(Integer, primary_key=True, index=True)
    fleetPlates = Column(String, index=True)
    orderID = Column(Integer, index=True)
