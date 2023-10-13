from sqladmin import ModelView, Admin

from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from project.users.models import User
from project.aviasales.models import Flight, Ticket, Destination, Plane

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
    class UserAdmin(ModelView, model=User):
        name = "User"
        name_plural = "Users"
        icon = "fa-solid fa-user"
        category = "accounts"


class TicketAdmin(ModelView, model=Ticket):
    column_list = ('id', 'class_type', 'price', 'status')

    class TicketAdmin(ModelView, model=Ticket):
        name = "Ticket"
        name_plural = "Tickets"
        # icon = "fa-solid fa-user"
        category = "Flight"


class FlightAdmin(ModelView, model=Flight):
    column_list = ('flight_number', 'arrival_time', 'departure_time', 'plane',)

    class FlightAdmin(ModelView, model=Flight):
        name = "Flight"
        name_plural = "Flights"
        # icon = "fa-solid fa-user"
        category = "Flight"


class DestinationAdmin(ModelView, model=Destination):
    column_list = ('title', 'location')

    class DestinationAdmin(ModelView, model=Destination):
        name = "Destination"
        name_plural = "Destinations"
        # icon = "fa-solid fa-user"
        category = "Flight"


class PlaneAdmin(ModelView, model=Plane):
    column_list = ('model', 'country', 'capacity')

    class PlaneAdmin(ModelView, model=Plane):
        name = "Plane"
        name_plural = "Planes"
        # icon = "fa-solid fa-user"
        category = "Flight"
