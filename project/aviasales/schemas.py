from pydantic import BaseModel


class SearchCriteria(BaseModel):
    destination: str
    departure: str
    departure_date: str
    count: str
    class_type: str

class TicketPurchase(BaseModel):
    ticket_id : int