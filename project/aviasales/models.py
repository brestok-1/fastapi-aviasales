from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from project.database import Base


class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String)

    flights = relationship("Flight", back_populates="destination")

    # def __str__(self):
    #     return f'{self.title} | Location : {self.location}'


class Plane(Base):
    __tablename__ = 'planes'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, index=True)
    country = Column(String)
    capacity = Column(Integer)

    flights = relationship("Flight", back_populates="plane")

    # def __str__(self):
    #     return f'{self.model} | Capacity : {self.capacity}'


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    class_type = Column(String, index=True, default='economy')
    price = Column(Float)
    status = Column(String, default='available')

    flight_id = Column(Integer, ForeignKey('flights.id'))
    flight = relationship("Flight", back_populates="tickets")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tickets")

    # def __str__(self):
    #     return f'Ticket | Class : {self.class_type} | price : {self.price}$'


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)

    destination_id = Column(Integer, ForeignKey('destinations.id'))
    destination = relationship("Destination", back_populates="flights")

    plane_id = Column(Integer, ForeignKey('planes.id'))
    plane = relationship("Plane", back_populates="flights")

    tickets = relationship("Ticket", back_populates="flight")

    # def __str__(self):
    #     return f'Flight | Number : {self.flight_number} | Plane : {self.plane.model}'
