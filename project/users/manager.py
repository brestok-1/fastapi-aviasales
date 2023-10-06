import os
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from project.database import get_user_db
from project.users.models import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = os.getenv('SECRET')
    verification_token_secret = os.getenv('SECRET')

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
