from data.database import insert_query, read_query, update_query
from data.models import Developer, Project


def all(name: str | None = None, limit: int | None = None, status: str | None = None):
    data = read_query('''SELECT id, name, is_open, team_limit
FROM projects
ORDER BY id;''')
    result = [Project.from_query_result(*row) for row in data]

    if name is not None:
        result = [p for p in result if name.lower() in p.name.lower()]

    if limit is not None:
        result = [p for p in result if p.limit <= limit]

    if status is not None:
        result = [p for p in result if p.status == status]

    return result


def get_by_id(id: int):
    data = read_query('''SELECT id, name, is_open, team_limit
FROM projects
WHERE id = ?;''', (id,))

    return next((Project.from_query_result(*row) for row in data), None)


def exists_by_name(name: str):
    data = read_query('''SELECT id
FROM projects
WHERE name = ?;''', (name,))

    return len(data) > 0


def get_devs(project_id: int):
    data = read_query('''SELECT d.id, d.name, d.level
FROM devs d
JOIN devs_projects dp ON d.id = dp.dev_id
WHERE dp.project_id = ?
ORDER BY d.id;''', (project_id,))

    return [Developer.from_query_result(*row) for row in data]


def create(project: Project):
    project.id = insert_query('''INSERT INTO projects (name, is_open, team_limit)
VALUES (?, ?, ?);''', (project.name, int(project.status == 'open'), project.limit))

    return project


def set_status(project: Project, status: str):
    update_query('''UPDATE projects
SET is_open = ?
WHERE id = ?;''', (int(status == 'open'), project.id))
    project.status = status

    return project


def assign_dev(project_id: int, dev_id: int):
    insert_query('''INSERT INTO devs_projects (dev_id, project_id)
VALUES (?, ?);''', (dev_id, project_id))


def remove_dev(project_id: int, dev_id: int):
    return update_query('''DELETE FROM devs_projects
WHERE dev_id = ? AND project_id = ?;''', (dev_id, project_id))


def create_project_response(project: Project):
    return {
        'id': project.id,
        'name': project.name,
        'status': project.status,
        'limit': project.limit,
        'devs': get_devs(project.id)
    }
