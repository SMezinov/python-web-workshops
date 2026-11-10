from fastapi import FastAPI
from data.database import init_database
from routers.devs import devs_router
from routers.projects import projects_router


init_database()

app = FastAPI()
app.include_router(projects_router)
app.include_router(devs_router)
