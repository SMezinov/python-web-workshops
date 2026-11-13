from data.database import insert_query, read_query
from data.models import Category


def all():
    data = read_query('select id, name from categories order by id')

    return (Category(id=id, name=name) for id, name in data)


def get_by_id(id: int):
    data = read_query('select id, name from categories where id = ?', (id,))

    return next((Category(id=id, name=name) for id, name in data), None)


def exists(id: int):
    return any(
        read_query(
            'select id, name from categories where id = ?',
            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name) values(?)',
        (category.name,))

    category.id = generated_id

    return category
