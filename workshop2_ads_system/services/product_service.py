from data.database import read_query, update_query, insert_query
from math import ceil

from data.models import Product
from services.profile_service import get_profile_by_id

def get_product_category_id(product_id: int) -> int | None:
    data = read_query('''SELECT category_id FROM products WHERE id = ?''',
                      (product_id,)
                      )
    if not data:
        return None

    category_id = data[0][0]
    return category_id


def get_interest_relevance(profile_id: int, category_id: int) -> int | None:
    data = read_query('''SELECT relevance FROM interests WHERE profile_id = ? AND category_id = ?''',
                      (profile_id, category_id)
                      )
    if not data:
        return None

    relevance = data[0][0]
    return relevance


def calculate_new_relevance(relevance: int) -> int:
    new_relevance = ceil(relevance + (relevance * 0.05))
    return new_relevance


def update_interests_relevance(profile_id: int, category_id: int, new_relevance: int) -> bool:
    is_updated = update_query('''UPDATE interests SET relevance = ? WHERE profile_id = ? AND category_id = ?''',
                              (new_relevance, profile_id, category_id))

    return is_updated


def create_interests(profile_id: int, category_id: int):
    insert_query('''INSERT INTO interests(profile_id, category_id, relevance) VALUES (?, ?, ?)''',
                        (profile_id, category_id, 1))

def view_product(profile_id: int, product_id: int) -> bool:
    category_id = get_product_category_id(product_id)
    if category_id is None:
        return False

    profile = get_profile_by_id(profile_id)
    if profile is None:
        return False

    interest_relevance = get_interest_relevance(profile_id, category_id)
    if interest_relevance is not None:
        new_relevance = calculate_new_relevance(interest_relevance)
        update_interests_relevance(profile_id, category_id, new_relevance)
    else:
        create_interests(profile_id, category_id)

    return True


def get_random_product_from_categories(top_categories: list[int]) -> Product | None:
    if not top_categories:
        return None

    placeholders = ', '.join('?' for _ in top_categories)

    data = read_query(f'''SELECT id, name, price, category_id FROM products WHERE category_id IN ({placeholders}) ORDER BY RANDOM() LIMIT 1''',
                      (tuple(top_categories))
                      )

    if not data:
        return None

    return Product.from_query_result(*data[0])

def get_random_product() -> Product | None:
    data = read_query('''SELECT id, name, price, category_id FROM products ORDER BY RANDOM() LIMIT 1''',)

    if not data:
        return None

    return Product.from_query_result(*data[0])