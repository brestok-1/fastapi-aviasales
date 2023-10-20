from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from project.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)

    tickets = relationship("Ticket", back_populates="user")

    def __str__(self):
        return f'{self.username}'