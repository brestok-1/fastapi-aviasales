from fastapi import APIRouter

from project.users.auth import fastapi_users

current_user = fastapi_users.current_user()
current_superuser = fastapi_users.current_user(active=True, superuser=True)

user_router = APIRouter(
    prefix='/user'
)

from project.users import models, views
