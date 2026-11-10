from fastapi import APIRouter, Response
from data.models import Project, ProjectStatus
from services import dev_service, project_service


projects_router = APIRouter(prefix='/projects')


@projects_router.get('')
def get_projects(name: str | None = None, limit: int | None = None, status: str | None = None):
    if status is not None and status not in ('open', 'closed'):
        return Response(status_code=400, content='Status must be open or closed')

    return project_service.all(name, limit, status)


@projects_router.get('/{id}')
def get_project_by_id(id: int):
    project = project_service.get_by_id(id)

    if project is None:
        return Response(status_code=404)

    return project_service.create_project_response(project)


@projects_router.post('', status_code=201)
def create_project(project: Project):
    project.name = project.name.strip()

    if project.name == '':
        return Response(status_code=400, content='Name cannot be empty')

    if project.status not in ('open', 'closed'):
        return Response(status_code=400, content='Status must be open or closed')

    if project.limit <= 0:
        return Response(status_code=400, content='Limit must be a positive integer')

    if project_service.exists_by_name(project.name):
        return Response(status_code=400, content='Project name already exists')

    return project_service.create(project)


@projects_router.put('/{id}/status')
def set_project_status(id: int, data: ProjectStatus):
    project = project_service.get_by_id(id)

    if project is None:
        return Response(status_code=404)

    if data.status not in ('open', 'closed'):
        return Response(status_code=400, content='Status must be open or closed')

    return project_service.set_status(project, data.status)


@projects_router.post('/{project_id}/devs/{dev_id}', status_code=201)
def assign_dev_to_project(project_id: int, dev_id: int):
    project = project_service.get_by_id(project_id)
    dev = dev_service.get_by_id(dev_id)

    if project is None or dev is None:
        return Response(status_code=404)

    if project.status == 'closed':
        return Response(status_code=400, content='Cannot assign devs to a closed project')

    assigned_devs = project_service.get_devs(project_id)

    if any(d.id == dev_id for d in assigned_devs):
        return Response(status_code=400, content='Developer is already assigned to this project')

    if len(assigned_devs) >= project.limit:
        return Response(status_code=400, content='Project limit is reached')

    if dev.level != 'senior':
        if dev_service.get_projects(dev_id):
            return Response(status_code=400, content='Only senior devs can join more than one project')

        if not any(d.level == 'senior' for d in assigned_devs):
            return Response(status_code=400, content='Project must have at least one senior dev')

    project_service.assign_dev(project_id, dev_id)

    return project_service.create_project_response(project)


@projects_router.delete('/{project_id}/devs/{dev_id}', status_code=204)
def remove_dev_from_project(project_id: int, dev_id: int):
    project = project_service.get_by_id(project_id)
    dev = dev_service.get_by_id(dev_id)

    if project is None or dev is None:
        return Response(status_code=404)

    if not project_service.remove_dev(project_id, dev_id):
        return Response(status_code=404)

    return Response(status_code=204)
