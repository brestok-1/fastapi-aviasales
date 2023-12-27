import os
import uuid
from fastapi import Request

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.password import PasswordHelper
from sqladmin.authentication import AuthenticationBackend as AuthBackendAdmin

from project.users.manager import get_user_manager
from project.users.models import User

from sqlalchemy import select

cookie_transport = CookieTransport(
    cookie_name="aviasales",
    cookie_max_age=3600,  # 1 hour
    cookie_path="/",
    cookie_domain=None,  # По умолчанию, используйте None, чтобы ограничить куки текущим доменом
    cookie_secure=False,  # Во время разработки можете использовать False, но в боевой среде используйте True с HTTPS
    cookie_httponly=False,  # Рекомендуется использовать True для безопасности
    cookie_samesite="lax",  # Рекомендуется использовать "lax" для безопасности
)


def get_jwt_strategy() -> JWTStrategy:
    # Возвращаем объект JWTStrategy
    return JWTStrategy(secret=os.getenv('SECRET'), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


class AdminAuth(AuthBackendAdmin):
    async def login(self, request: Request) -> bool:
        from project import async_session_maker

        form = await request.form()
        # Получаем почту и пароль из формы
        email, password = form["email"], form["password"]
        password_helper = PasswordHelper()
        async with async_session_maker() as session:
            # Получаем пользователя с введенным email
            user = await session.execute(select(User).where(User.email == email))
            user = user.scalar_one_or_none()
            # Если пользователь существует и пароль верный, то добавляем токен доступа
            if user and password_helper.verify_and_update(password, user.hashed_password)[0] and user.is_superuser:
                request.session.update({"session": str(uuid.uuid4())})
                return True
            else:
                return False

    async def logout(self, request: Request) -> bool:
        # Удаляем токен доступа
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Получаем токен
        token = request.session.get("session")

        if not token:
            return False
        return True


authentication_backend_admin = AdminAuth(secret_key=os.getenv('SECRET'))

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
