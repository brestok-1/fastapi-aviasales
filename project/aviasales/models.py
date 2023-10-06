from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.database import Base


class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String)

    flights = relationship("Flight", back_populates="destination")


class Plane(Base):
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    country = Column(String)
    capacity = Column(Integer)

    flights = relationship("Flight", back_populates="plane")


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)
    departure_date = Column(String)
    departure_time = Column(String)
    arrival_time = Column(String)
    business_tickets_left = Column(Integer)
    business_ticket_price = Column(Float)
    economy_tickets_left = Column(Integer)
    economy_ticket_price = Column(Float)

    destination_id = Column(Integer, ForeignKey('destinations.id'))
    destination = relationship("Destination", back_populates="flights")

    plane_id = Column(Integer, ForeignKey('planes.id'))
    plane = relationship("Plane", back_populates="flights")
