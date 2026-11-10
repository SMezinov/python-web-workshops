from fastapi import APIRouter, HTTPException
from data.models import Product
from services.ad_service import serve_ad


ads_router = APIRouter(prefix='/ads', tags=['ads'])

@ads_router.get('/{ip_address}', response_model=Product)
def ads(ip_address: str):
    product = serve_ad(ip_address)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail='No product available'
        )

    return product