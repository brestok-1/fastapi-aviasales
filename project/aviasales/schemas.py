from pydantic import BaseModel


class SearchCriteria(BaseModel):
    departure: str
    destination: str
    departure_date: str
    count: str
    class_type: str


class TicketPurchase(BaseModel):
    id: int


class TicketsPurchase(BaseModel):
    flight_id: int
    class_type: str
    count: int
