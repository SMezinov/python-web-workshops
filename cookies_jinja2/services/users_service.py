from data.database import insert_query, read_query, update_query
from data.models import Order, Role, User
from hashlib import sha256
from mariadb import IntegrityError

_SEPARATOR = ';'


def _hash_password(password: str):
       return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    password = _hash_password(password)
    return user if user and user.password == password else None


def create(username: str, password: str) -> User | None:
    password = _hash_password(password)
    try:
        generated_id = insert_query(
            'INSERT INTO users(username, password, role) VALUES (?,?,?)',
            (username, password, Role.CUSTOMER))

        return User(id=generated_id, username=username, password='', role=Role.CUSTOMER)

    except IntegrityError:
        return None


def create_token(user: User) -> str:
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        token.split(_SEPARATOR)))


def from_token(token: str) -> User | None:
    if token:
        _, username = token.split(_SEPARATOR)

        return find_by_username(username)


def owns_order(user: User, order: Order) -> bool:
    return order.user_id == user.id

def delete_user_by_username(username: str) -> bool:
    result = update_query('''DELETE FROM users
WHERE username = ?;''', (username, ))
    return result