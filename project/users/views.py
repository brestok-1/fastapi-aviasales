from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from project.users import user_router

template = Jinja2Templates(directory='project/users/templates')


@user_router.get('/login', name='login')
async def login(request: Request):
    return template.TemplateResponse("login.html", {'request': request})


@user_router.get('/sign-up', name='sign-up')
async def sign_up(request: Request):
    return template.TemplateResponse("registration.html", {'request': request})
