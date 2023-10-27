from fastapi import APIRouter

avia_router = APIRouter(
    prefix=''
)

from . import models, views
