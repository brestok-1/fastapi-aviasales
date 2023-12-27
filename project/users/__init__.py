from fastapi import APIRouter

from project.users.auth import fastapi_users

current_user = fastapi_users.current_user() # Получаем объект текущего пользователя
current_superuser = fastapi_users.current_user(active=True, superuser=True)

# Создаем APIRouter
user_router = APIRouter(
    prefix='/user'
)

# Импортируем контроллеры и модели
from project.users import models, views
