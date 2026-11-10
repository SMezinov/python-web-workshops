from fastapi import APIRouter, Response
from data.models import Developer, LEVELS
from services import dev_service


devs_router = APIRouter(prefix='/devs')


@devs_router.get('')
def get_devs(name: str | None = None, level: str | None = None):
    if level is not None and level not in LEVELS:
        return Response(status_code=400, content='Level must be junior, mid or senior')

    return dev_service.all(name, level)


@devs_router.get('/{id}')
def get_dev_by_id(id: int):
    dev = dev_service.get_by_id(id)

    if dev is None:
        return Response(status_code=404)

    return dev_service.create_dev_response(dev)


@devs_router.post('', status_code=201)
def create_dev(dev: Developer):
    dev.name = dev.name.strip()

    if dev.name == '':
        return Response(status_code=400, content='Name cannot be empty')

    if dev.level not in LEVELS:
        return Response(status_code=400, content='Level must be junior, mid or senior')

    if dev_service.exists_by_name(dev.name):
        return Response(status_code=400, content='Developer name already exists')

    return dev_service.create(dev)
