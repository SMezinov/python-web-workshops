import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from data.models import Order, User
from data.database import read_query, insert_query
from pwdlib import PasswordHash

load_dotenv()
password_hash = PasswordHash.recommended()

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"

def find_by_username(username: str) -> User | None:
    data = read_query('''
    SELECT id, username, role
    FROM users
    WHERE username = ?;''',
                      (username,)
    )

    if not data:
        return None

    row = data[0]

    order_rows = read_query(
        """SELECT id
           FROM orders
           WHERE user_id = ?;""",
        (row[0],)
    )

    order_ids = [order_row[0] for order_row in order_rows]

    user = User(id=row[0], username=row[1], role=row[2], orders=order_ids)

    return user

def create_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token


def is_authenticated(token: str) -> bool:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp"]}
        )

        user_id = int(payload["sub"])

        data = read_query('''SELECT id 
                             FROM users 
                             WHERE id = ?;''',
        (user_id,)
        )

        return bool(data)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return False


def from_token(token: str) -> User | None:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["sub", "exp"]}
        )

        user_id = int(payload["sub"])
        username_data = read_query('''SELECT username
                             FROM users
                             WHERE id = ?;''',
                          (user_id,)
                          )

        if not username_data:
            return None

        return find_by_username(username_data[0][0])

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None



def owns_order(user: User, order: Order) -> bool:
    return order.id in user.orders

def register(username: str, password: str) -> User:
    hashed_password = password_hash.hash(password)

    user_id = insert_query('''
    INSERT INTO users (username, password_hash, role) VALUES(?, ?, ?)''',
                 (username, hashed_password, "Customer")
    )

    user = User(id=user_id, username=username, role='Customer', orders=[])

    return user

def verify_credentials(username: str, password: str) -> bool:
    data = read_query('''SELECT password_hash FROM users WHERE username = ?''',
                      (username, )
                      )
    if not data:
        return False

    return password_hash.verify(password, data[0][0])