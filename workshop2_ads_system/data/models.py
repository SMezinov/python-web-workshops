from pydantic import BaseModel

class Profile(BaseModel):
    id: int
    ip_address: str
    country_code: str

    @classmethod
    def from_query_result(cls, id, ip_address, country_code):
        return cls(id=id, ip_address=ip_address, country_code=country_code)


class Category(BaseModel):
    id: int
    name: str
    cumulative_relevance: int

    @classmethod
    def from_query_result(cls, id, name, cumulative_relevance):
        return cls(id=id, name=name, cumulative_relevance=cumulative_relevance)

class FavouriteCategory(BaseModel):
    id: int
    name: str
    relevance: int
    @classmethod
    def from_query_result(cls, id, name, relevance):
        return cls(id=id, name=name, relevance=relevance)

class Interest(BaseModel):
    profile_id: int
    category_id: int
    relevance: int


class Product(BaseModel):
    id: int
    name: str
    price: float
    category_id: int

    @classmethod
    def from_query_result(cls, id, name, price, category_id):
        return cls(id=id, name=name, price=price, category_id=category_id)


class ExtendedProfile(BaseModel):
    profile: Profile
    categories: list[FavouriteCategory]