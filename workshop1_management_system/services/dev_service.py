from data.database import insert_query, read_query
from data.models import Developer, LEVELS, Project


def all(name: str | None = None, level: str | None = None):
    data = read_query('''SELECT id, name, level
FROM devs
ORDER BY id;''')
    result = [Developer.from_query_result(*row) for row in data]

    if name is not None:
        result = [d for d in result if name.lower() in d.name.lower()]

    if level is not None:
        result = [d for d in result if d.level == level]

    return result


def get_by_id(id: int):
    data = read_query('''SELECT id, name, level
FROM devs
WHERE id = ?;''', (id,))

    return next((Developer.from_query_result(*row) for row in data), None)


def exists_by_name(name: str):
    data = read_query('''SELECT id
FROM devs
WHERE name = ?;''', (name,))

    return len(data) > 0


def get_projects(dev_id: int):
    data = read_query('''SELECT p.id, p.name, p.is_open, p.team_limit
FROM projects p
JOIN devs_projects dp ON p.id = dp.project_id
WHERE dp.dev_id = ?
ORDER BY p.id;''', (dev_id,))

    return [Project.from_query_result(*row) for row in data]


def create(dev: Developer):
    dev.id = insert_query('''INSERT INTO devs (name, level)
VALUES (?, ?);''', (dev.name, LEVELS.index(dev.level) + 1))

    return dev


def create_dev_response(dev: Developer):
    return {
        'id': dev.id,
        'name': dev.name,
        'level': dev.level,
        'projects': get_projects(dev.id)
    }
