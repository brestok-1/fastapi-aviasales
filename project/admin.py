from sqladmin import ModelView

from project.users.models import User
from project.aviasales.models import Flight


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email]

    class UserAdmin(ModelView, model=User):
        name = "User"
        name_plural = "Users"
        icon = "fa-solid fa-user"
        category = "accounts"


class TicketAdmin(ModelView, model=Flight):
    pass
