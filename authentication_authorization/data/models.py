from datetime import date
from typing import Annotated
from pydantic import BaseModel, StringConstraints, constr, Field
from pwdlib import PasswordHash

class Category(BaseModel):
    id: int | None = None
    name: str


class Product(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: float
    category_id: int

    @classmethod
    def from_query_result(cls, id, name, description, price, category_id):
        return cls(
            id=id,
            name=name,
            description=description,
            price=price,
            category_id=category_id)


class Order(BaseModel):
    id: int | None = None
    product_ids: list[int] = []
    delivery_date: date
    delivery_address: str | None = None

    @classmethod
    def from_query_result(cls, id, delivery_date, delivery_address, product_ids=[]):
        return cls(
            id=id,
            delivery_date=delivery_date,
            delivery_address=delivery_address,
            product_ids=product_ids)


class OrderUpdate(BaseModel):
    delivery_date: date
    delivery_address: str | None = None


TUsername = Annotated[str, StringConstraints(pattern=r'^\w{2,30}$')] # constr(regex='^\w{2,30}$')


class User(BaseModel):
    id: int | None = None
    username: TUsername
    role: str
    orders: list[int] = []

    def is_admin(self):
        return self.role == 'Admin'


class LoginData(BaseModel):
    username: TUsername
    password: str = Field(min_length=8)
