from fastapi import APIRouter, Request
from services import product_service, category_service
from common.template_config import CustomJinja2Templates

product_router = APIRouter(prefix='/products')
templates = CustomJinja2Templates(directory='templates')

@product_router.get('')
def get_products(request: Request):
    products = list(product_service.all())
    categories_dict = category_service.categories_dict()

    return templates.TemplateResponse(request=request, name='products.html', context={'products': products, 'categories': categories_dict})

@product_router.get('/{id}')
def get_product_by_id(request: Request, id: int):
    product = product_service.get_by_id(id)
    return templates.TemplateResponse(request=request, name='single-product.html', context={'product': product})

