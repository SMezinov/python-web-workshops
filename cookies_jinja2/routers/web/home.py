from fastapi import APIRouter, Request
from common.template_config import CustomJinja2Templates

index_router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')

@index_router.get('/')
def index(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')