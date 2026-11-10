from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.api.product import product_router as api_product_router
from routers.api.categories import categories_router as api_categories_router
from routers.api.orders import orders_router as api_orders_router
from routers.api.users import users_router as api_users_router
from routers.web.products import product_router
from routers.web.home import index_router
from routers.web.categories import category_router

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(api_product_router)
app.include_router(api_categories_router)
app.include_router(api_orders_router)
app.include_router(api_users_router)
app.include_router(product_router)
app.include_router(index_router)
app.include_router(category_router)