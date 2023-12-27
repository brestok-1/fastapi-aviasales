from typing import Any

from fastapi_users.password import PasswordHelper
from sqladmin import ModelView

from fastapi import Request

from project.users.models import User
from project.aviasales.models import Flight, Ticket, Location, Plane
from project.custom_admin import CustomQuery


# Класс административной панели для управления моделью User
class UserAdmin(ModelView, model=User):
    column_list = column_sortable_list = [User.id, User.username, User.email]
    is_async = True
    icon = "fa-solid fa-user"
    category = "Account"
    name = "User"
    name_plural = "Users"
    column_searchable_list = [User.username]
    column_details_exclude_list = [User.hashed_password, 'is_active', 'is_verified']
    form_excluded_columns = ['is_active', 'is_verified', 'is_superuser', 'tickets']
    column_export_list = ['id', 'email', 'username', 'is_superuser']

    # Метод, выполняемый при удалении модели User
    async def on_model_delete(self, model: Any) -> bool:
        return not model.is_superuser

    # Метод для удаления модели
    async def delete_model(self, request: Request, pk: Any) -> None:
        await CustomQuery(self).delete(pk)

    # Метод, выполняемый при изменении модели User
    async def on_model_change(self, data: dict, model: Any, is_created: bool) -> dict:
        if is_created:
            # Хеширование пароля перед сохранением
            password_helper = PasswordHelper()
            password = data['hashed_password']
            hashed_password = password_helper.hash(password)
            data['hashed_password'] = hashed_password
            data['is_active'] = True
        return data

    # Метод для вставки модели
    async def insert_model(self, request: Request, data: dict) -> Any:
        return await CustomQuery(self).insert(data)


# Класс административной панели для управления моделью Ticket
class TicketAdmin(ModelView, model=Ticket):
    is_async = True
    column_list = column_sortable_list = ('id', 'class_type', 'price', 'status')
    name = "Ticket"
    name_plural = "Tickets"
    icon = "fa-solid fa-ticket"
    category = "Flight"


# Класс административной панели для управления моделью Location
class LocationAdmin(ModelView, model=Location):
    is_async = True
    column_list = column_sortable_list = ('title', 'location')
    name = "Location"
    name_plural = "Locations"
    icon = "fa-solid fa-location-dot"
    category = "Flight"
    column_searchable_list = [Location.title, Location.location]


# Класс административной панели для управления моделью Plane
class PlaneAdmin(ModelView, model=Plane):
    is_async = True
    column_list = column_sortable_list = ('model', 'country', 'capacity')
    name = "Plane"
    name_plural = "Planes"
    icon = "fa-solid fa-plane"
    category = "Flight"
    column_searchable_list = [Plane.country]


# Класс административной панели для управления моделью Flight
class FlightAdmin(ModelView, model=Flight):
    is_async = True
    column_list = column_sortable_list = ('flight_number', 'arrival_time', 'departure_time', 'plane',)
    name = "Flight"
    name_plural = "Flights"
    icon = "fa-solid fa-plane-circle-exclamation"
    category = "Flight"
    column_searchable_list = [Flight.flight_number]
