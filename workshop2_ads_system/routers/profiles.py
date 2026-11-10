from fastapi import APIRouter, HTTPException
from data.models import Profile, ExtendedProfile
from services.profile_service import get_all_profiles,get_country_codes, get_extended_profile
from services.product_service import view_product

profiles_router = APIRouter(prefix='/profiles', tags=['profiles'])

@profiles_router.get('/', response_model=list[Profile])
def all_profiles(country_code: str | None = None):
    return get_all_profiles(country_code)

@profiles_router.get('/country_codes', response_model=list[str])
def get_codes():
    return get_country_codes()

@profiles_router.get('/{id}', response_model=ExtendedProfile)
def get_profile(id: int):
    extended_profile = get_extended_profile(id)
    if extended_profile is None:
        raise HTTPException(
            status_code=404,
            detail='Profile not found'
        )
    return extended_profile

@profiles_router.post('/{profile_id}/products/{product_id}/views', status_code=204)
def view(profile_id: int, product_id: int):
    success = view_product(profile_id, product_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail='Profile or product not found'
        )
