from fastapi import Depends, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import and_, or_
from . import avia_router
from .models import Ticket, Flight, Location
from project.database import get_async_session
from project.users.models import User
from .schemas import SearchCriteria, TicketPurchase
from ..users import current_user

template = Jinja2Templates(directory='project/aviasales/templates')


@avia_router.get('/', name='main')
async def main(request: Request):
    return template.TemplateResponse("main.html", {'request': request})


@avia_router.get('/search-flights/', name='search-flights')
async def get_founded_flights(departure: str = Query(...),
                              destination: str = Query(...),
                              departure_date: str = Query(...),
                              count: str = Query(...),
                              class_type: str = Query(...),
                              session: AsyncSession = Depends(get_async_session)
                              ):
    departure_datetime = datetime.strptime(departure_date, "%d-%m-%Y").date()
    departure_destination_date_flights = await session.execute(
        select(Flight).options(
            selectinload(Flight.departure),
            selectinload(Flight.destination),
            selectinload(Flight.tickets),
            selectinload(Flight.plane)
        )
        .filter(
            Flight.departure.has(Location.location.ilike(f"%{departure.lower()}%")),
            Flight.destination.has(Location.location.ilike(f"%{destination.lower()}%")),
            func.date(Flight.departure_time) == departure_datetime
        )
    )
    departure_destination_date_flights = departure_destination_date_flights.scalars().all()
    if not departure_destination_date_flights:
        return JSONResponse(content={
            'message': f'Nothing was found for your query'},
            status_code=404)
    flights_full_data = []
    for flight in departure_destination_date_flights:
        flight_data = {}
        tickets = flight.tickets
        tickets_class_type = list(
            filter(lambda x: x.class_type == class_type and x.status == 'available', tickets))
        if tickets_class_type and len(tickets_class_type) >= int(count):
            flight_data['tickets_count'] = len(tickets_class_type)
            flight_data['tickets_price'] = tickets_class_type[0].price
            flight_data['flight'] = flight
        flights_full_data.append(flight_data)
    if departure_destination_date_flights and not flights_full_data[0]:
        not_selected_class_type = 'Economy' if class_type == 'Business' else 'Business'
        return JSONResponse(content={
            'message': f'Flights with the selected ticket class and quantity are not available.'
                       f' Try to choose tickets among {not_selected_class_type} class or reduce quantity'},
            status_code=404)
    return flights_full_data


@avia_router.get('/search/', name='search')
async def get_search_list(request: Request,
                          search_criteria: SearchCriteria = Depends()):
    return template.TemplateResponse("search.html", {'request': request})


@avia_router.get('/latest-flights', name='latest-flights', dependencies=[Depends(current_user)])
async def get_latest_flights(session: AsyncSession = Depends(get_async_session)):
    latest_flights = await session.execute(select(Flight).options(
        selectinload(Flight.departure),
        selectinload(Flight.destination),
        selectinload(Flight.tickets),
        selectinload(Flight.plane)
    ).filter(
        Flight.tickets.any(and_(Ticket.status == 'available', Ticket.class_type == 'economy'))
    ))
    latest_flights = latest_flights.scalars().all()
    try:
        return latest_flights[:5]
    except IndexError:
        return latest_flights[:len(latest_flights) - 1]


@avia_router.post('/purchase', name='buy-ticket')
async def buy_chosen_ticket(ticket: TicketPurchase,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user)):
    chosen_ticket = await session.execute(select(Ticket).where(Ticket.id == ticket.id))
    chosen_ticket = chosen_ticket.scalars().one()
    chosen_ticket.status = 'purchased'
    chosen_ticket.user = user
    session.add(chosen_ticket)
    await session.commit()


@avia_router.get('/purchase-history', name='purchase-history')
async def get_purchase_history(session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user)):
    tickets = await session.execute(select(Ticket).join(Ticket.flight).options(
        joinedload(Ticket.flight).joinedload(Flight.destination),
        joinedload(Ticket.flight).joinedload(Flight.departure)
    ).where(Ticket.user == user))
    tickets = tickets.scalars().all()
    purchase_data = []
    for ticket in tickets:
        temp_data = {}
        ticket_flight = ticket.flight
        temp_data['flight_id'] = ticket_flight.flight_number
        temp_data['price'] = ticket.price
        temp_data['departure'] = ticket_flight.departure.location
        temp_data['destination'] = ticket_flight.destination.location
        temp_data['class_type'] = ticket.class_type
        temp_data['departure_time'] = ticket_flight.departure_time
        temp_data['arrival_time'] = ticket_flight.arrival_time
        purchase_data.append(temp_data)

    return purchase_data
