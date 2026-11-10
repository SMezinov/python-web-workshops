from fastapi import FastAPI
from routers.product import product_router
from routers.categories import categories_router
from routers.orders import orders_router
from routers.users import users_router


app = FastAPI()
app.include_router(product_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(users_router)
