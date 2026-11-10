from data.models import Product
from services.profile_service import get_profile_id_by_ip_address
from services.product_service import get_random_product, get_random_product_from_categories
from services.category_service import get_top_categories

def serve_ad(ip_address: str) -> Product | None:
    profile_id = get_profile_id_by_ip_address(ip_address)
    if profile_id is not None:
        top_categories = get_top_categories(profile_id)
        random_product = get_random_product_from_categories(top_categories)
        if random_product is not None:
            return random_product

    return get_random_product()