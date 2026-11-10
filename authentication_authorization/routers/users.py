from fastapi import APIRouter, Header, HTTPException
from common.auth import get_user_or_raise_401
from data.models import LoginData
from services import users_service


users_router = APIRouter(prefix='/users')

@users_router.post('/register', status_code=201)
def register(data: LoginData):
    if users_service.find_by_username(data.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    user = users_service.register(data.username, data.password)

    return user

@users_router.post('/login')
def login(data: LoginData):
    if not users_service.verify_credentials(data.username, data.password):
        raise HTTPException(
    status_code=401,
    detail="Invalid username or password"
)

    user = users_service.find_by_username(data.username)
    token = users_service.create_token(user)

    return {"token": token}

@users_router.get('/info')
def user_info(x_token: str = Header()):
    return get_user_or_raise_401(x_token)

@users_router.get('/orders')
def user_orders(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return user.orders

