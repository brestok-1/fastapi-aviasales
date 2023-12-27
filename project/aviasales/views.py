import time
from datetime import datetime, timedelta, timezone
from fastapi import Depends, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import and_
from . import avia_router
from .models import Ticket, Flight, Location
from project.database import get_async_session
from project.users.models import User
from .schemas import SearchCriteria, TicketsPurchase
from .utils import create_updated_flight_dict
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
        tickets = flight.tickets
        tickets_class_type = list(
            filter(lambda x: x.class_type == class_type and x.status == 'available', tickets))
        if tickets_class_type and len(tickets_class_type) >= int(count):
            updated_flight = create_updated_flight_dict(flight.id,
                                                        flight.arrival_time,
                                                        flight.departure,
                                                        flight.departure_time,
                                                        flight.destination,
                                                        flight.flight_number,
                                                        flight.plane,
                                                        tickets_class_type[0].price,
                                                        class_type,
                                                        count)
            flights_full_data.append(updated_flight)
    if departure_destination_date_flights and not flights_full_data:
        # not_selected_class_type = 'Economy' if class_type == 'Business' else 'Business'
        flight_list = 'Available flight on chosen date:\n'
        count_available_flight = 0
        for flight in departure_destination_date_flights:
            flight_eco_tickets = []
            flight_business_tickets = []
            for ticket in flight.tickets:
                if ticket.status == 'available':
                    if ticket.class_type == 'business':
                        flight_business_tickets.append(ticket)
                    else:
                        flight_eco_tickets.append(ticket)
            flight_number = flight.flight_number
            business_ticket_count = len(flight_business_tickets)
            economy_ticket_count = len(flight_eco_tickets)
            if business_ticket_count or economy_ticket_count:
                flight_list += f'{flight_number} | Business: {business_ticket_count} | Economy: {economy_ticket_count}\n'
                count_available_flight += 1
        if count_available_flight:
            return JSONResponse(content={
                'message': f'Flights with the selected ticket class and quantity are not available. '
                           f'{flight_list}'}, status_code=404)
        else:
            return JSONResponse(content={
                'message': f'Nothing was found for your query'},
                status_code=404)
    return flights_full_data


@avia_router.get('/search/', name='search')
async def get_search_list(request: Request,
                          search_criteria: SearchCriteria = Depends()):
    return template.TemplateResponse("search.html", {'request': request})


@avia_router.get('/latest-flights', name='latest-flights')
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
    data = []
    for flight in latest_flights:
        tickets = flight.tickets
        ticket_id = 0
        ticket_price = 0
        for ticket in tickets:
            if ticket.class_type == 'economy' and ticket.status == 'available':
                ticket_price = ticket.price
                break
        updated_flight = create_updated_flight_dict(flight.id,
                                                    flight.arrival_time,
                                                    flight.departure,
                                                    flight.departure_time,
                                                    flight.destination,
                                                    flight.flight_number,
                                                    flight.plane,
                                                    ticket_price,
                                                    'economy',
                                                    1)
        data.append(updated_flight)
    try:
        return data[:5]
    except IndexError:
        return data[:len(data) - 1]


@avia_router.post('/purchase-tickets', name='buy-tickets')
async def buy_chosen_tickets(tickets: TicketsPurchase,
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    list_tickets = await session.execute(select(Ticket).filter(
        Ticket.flight_id == tickets.flight_id,
        Ticket.class_type == tickets.class_type,
        Ticket.status == 'available'
    ))
    list_tickets = list_tickets.scalars().all()[:tickets.count]
    if list_tickets:
        for ticket in list_tickets:
            ticket.status = 'purchased'
            ticket.user = user
        session.add_all(list_tickets)
        await session.commit()
        return True
    else:
        return False


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
        temp_data['ticket_id'] = ticket.id
        temp_data['flight_id'] = ticket_flight.flight_number
        temp_data['price'] = ticket.price
        temp_data['departure'] = ticket_flight.departure.location
        temp_data['destination'] = ticket_flight.destination.location
        temp_data['class_type'] = ticket.class_type
        temp_data['departure_time'] = ticket_flight.departure_time
        temp_data['arrival_time'] = ticket_flight.arrival_time
        purchase_data.append(temp_data)

    return purchase_data


@avia_router.get('/hi')
async def get_hi():
    return {'message': 'hello'}
