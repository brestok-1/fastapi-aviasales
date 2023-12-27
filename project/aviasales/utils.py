def create_updated_flight_dict(flight_id, arrival_time, departure, departure_time, destination, flight_number, plane,
                               ticket_price, class_type, ticket_count) -> dict:
    flight_time = arrival_time - departure_time
    print(flight_time)
    updated_flight = {
        'id': flight_id,
        'arrival_time': arrival_time,
        'departure': departure,
        'departure_time': departure_time,
        'destination': destination,
        'flight_number': flight_number,
        'plane': plane,
        'ticket_price': ticket_price,
        'class_type': class_type,
        'ticket_count': int(ticket_count),
        'flight_time': flight_time
    }
    return updated_flight
