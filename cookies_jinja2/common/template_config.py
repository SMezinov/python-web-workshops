from fastapi.templating import Jinja2Templates
from common.auth import get_user_if_token, get_user_or_raise_401
from services.users_service import is_authenticated



class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = get_user_if_token
        self.env.globals['get_user_or_raise_401'] = get_user_or_raise_401
        self.env.globals['is_authenticated'] = is_authenticated