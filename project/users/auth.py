import os

from fastapi import Request, Depends

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users.password import PasswordHelper
from sqladmin.authentication import AuthenticationBackend as AuthBackendAdmin
from sqlalchemy.ext.asyncio import AsyncSession

from project.users.manager import get_user_manager
from project.users.models import User

from sqlalchemy import select

cookie_transport = CookieTransport(cookie_name="aviasales", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
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
        email, password = form["email"], form["password"]
        password_helper = PasswordHelper()
        async with async_session_maker() as session:
            user = await session.execute(select(User).where(User.email == email))
            user: User = user.scalar_one()
            if user and password_helper.verify_and_update(password, user.hashed_password)[0] and user.is_superuser:
                request.session.update({"admin-token": "..."})
                return True
            else:
                return False
        # Validate username/password credentials
        # And update session

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("admin-token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend_admin = AdminAuth(secret_key=os.getenv('SECRET'))

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)
