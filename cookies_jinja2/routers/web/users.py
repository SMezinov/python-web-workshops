from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services import users_service
from common.auth import get_user_if_token
from common.template_config import CustomJinja2Templates

user_router = APIRouter(prefix='/users')
templates = CustomJinja2Templates(directory='templates')


@user_router.get('/login')
def serve_login(request: Request):
    page = templates.TemplateResponse(request=request, name='login.html')
    return page

@user_router.post('/login')
def user_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users_service.try_login(username, password)
    if user:
        token = users_service.create_token(user)
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name='login.html', context={'error': 'Invalid credentials'})



@user_router.post('/logout')
def user_logout(request: Request):
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie('token')
    return response



@user_router.get('/register')
def serve_register(request: Request):
    page = templates.TemplateResponse(request=request, name='register.html')
    return page


@user_router.post('/register')
def user_register(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users_service.create(username, password)
    if user:
        token = users_service.create_token(user)
        response = RedirectResponse(url='/', status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name='register.html', context={'error': 'This username already exists'})


@user_router.get('/info')
def user_info(request: Request):
    user = get_user_if_token(request)

    if user:
        return templates.TemplateResponse(request=request, name='users.html')
    else:
        response = RedirectResponse(url='/users/login')
        return response



@user_router.post('/delete')
def user_delete(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_if_token(request)
    hashed_password = users_service._hash_password(password)

    if user:
        if username == user.username and hashed_password == user.password:
            response = RedirectResponse(url='/', status_code=302)
            response.delete_cookie('token')
            users_service.delete_user_by_username(username)
            return response
        else:
            return templates.TemplateResponse(request=request, name='users.html', context={'error': 'Wrong username or password!'})
    else:
        response = RedirectResponse(url='/users/login', status_code=303)
        return response