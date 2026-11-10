from fastapi import APIRouter
from data.models import Category
from services.category_service import get_all_categories

categories_router = APIRouter(prefix='/categories', tags=['categories'])

@categories_router.get('/', response_model=list[Category])
def all_categories(country_code: str | None = None):
    categories = get_all_categories(country_code)
    return categories