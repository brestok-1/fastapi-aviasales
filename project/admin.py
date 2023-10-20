from sqladmin import ModelView, Admin

from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from project.users.models import User
from project.aviasales.models import Flight, Ticket, Location, Plane

template = Jinja2Templates(directory='project/users/templates')


class AdminCustom(Admin):
    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        context = {"request": request, "error": ""}

        if request.method == "GET":
            return template.TemplateResponse("login_admin.html", context)

        ok = await self.authentication_backend.login(request)
        if not ok:
            context["error"] = "Invalid credentials."
            return template.TemplateResponse(
                "login_admin.html", context, status_code=400
            )

        return RedirectResponse(request.url_for("admin:index"), status_code=302)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]
    can_create = False
    is_async = True
    icon = "fa-solid fa-user"
    category = "Account"
    name = "User"
    name_plural = "Users"


class TicketAdmin(ModelView, model=Ticket):
    is_async = True
    column_list = ('id', 'class_type', 'price', 'status')
    name = "Ticket"
    name_plural = "Tickets"
    icon = "fa-solid fa-ticket"
    category = "Flight"


class LocationAdmin(ModelView, model=Location):
    is_async = True
    column_list = ('title', 'location')
    name = "Location"
    name_plural = "Locations"
    icon = "fa-solid fa-location-dot"
    category = "Flight"


class PlaneAdmin(ModelView, model=Plane):
    is_async = True
    column_list = ('model', 'country', 'capacity')
    name = "Plane"
    name_plural = "Planes"
    icon = "fa-solid fa-plane"
    category = "Flight"


class FlightAdmin(ModelView, model=Flight):
    is_async = True
    column_list = ('flight_number', 'arrival_time', 'departure_time', 'plane',)
    name = "Flight"
    name_plural = "Flights"
    icon = "fa-solid fa-plane-circle-exclamation"
    category = "Flight"
