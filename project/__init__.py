from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Импортируем несколько классов и модулей из различных частей приложения
from project.admin import UserAdmin, TicketAdmin, FlightAdmin, LocationAdmin, PlaneAdmin
from project.custom_admin import AdminCustom
from project.config import settings, ORIGINS
from project.database import get_async_session, async_session_maker, engine
from project.users.auth import auth_backend, fastapi_users, authentication_backend_admin
from project.users.schemas import UserRead, UserCreate

# Создаем экземпляр FastAPI
def create_app() -> FastAPI:
    app = FastAPI()

    # Подключаем роутер для обработки запросов, связанных с авиабилетами
    from project.aviasales import avia_router
    app.include_router(avia_router, tags=['avia'])

    # Подключаем роутер для обработки запросов, связанных с пользователями
    from project.users import user_router
    app.include_router(user_router, tags=['Users'])

    # Подключаем роутеры для авторизации, регистрации и сброса пароля пользователей
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix='/auth',
        tags=['auth'],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    # Монтируем статические файлы (изображения, стили, скрипты) в URL-пространство "/static"
    app.mount('/static', StaticFiles(directory="static"), name="static")

    # Настраиваем CORS (Cross-Origin Resource Sharing) middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:3000", 'http://192.168.0.110:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Создаем экземпляр пользовательской административной панели и добавляем в нее виды (views)
    admin = AdminCustom(app, engine, authentication_backend=authentication_backend_admin)
    admin.add_view(TicketAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(FlightAdmin)
    admin.add_view(LocationAdmin)
    admin.add_view(PlaneAdmin)

    # Возвращаем созданный экземпляр FastAPI
    return app
