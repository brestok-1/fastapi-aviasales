from fastapi import APIRouter

avia_router = APIRouter(
    prefix=''
)

from . import models, views


# latest_flights = await session.execute(select(Flight).options(
#         selectinload(Flight.departure),
#         selectinload(Flight.destination),
#         selectinload(Flight.tickets),
#         selectinload(Flight.plane)
#     ).filter(
#         Flight.tickets.any(and_(Ticket.status == 'available', Ticket.class_type == 'economy'))
#     ))