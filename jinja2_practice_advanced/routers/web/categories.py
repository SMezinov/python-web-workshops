from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from services import category_service
from services import product_service

category_router = APIRouter(prefix='/categories')
templates = Jinja2Templates(directory='templates')

@category_router.get('')
def get_categories(request: Request):
    categories = list(category_service.all())
    return templates.TemplateResponse(request=request, name='categories.html', context={'categories': categories})

@category_router.get('/{id}')
def get_category_by_id(request: Request, id: int):
    category = category_service.get_by_id(id)
    products = list(product_service.get_by_category(category.id))
    return templates.TemplateResponse(request=request, name='single-category.html', context={'category': category, 'products': products})