from data.models import Profile, FavouriteCategory, ExtendedProfile
from data.database import read_query

def get_all_profiles(country_code: str | None = None) -> list[Profile]:
    if country_code is None:
        data = read_query('''SELECT id, ip_address, country_code FROM profiles''')
    else:
        data = read_query('''SELECT id, ip_address, country_code
                             FROM profiles WHERE country_code = ?''',
                          (country_code, )
                          )

    profiles = []
    for row in data:
        profiles.append(Profile.from_query_result(*row))

    return profiles


def get_country_codes() -> list[str]:
    data = read_query('''SELECT DISTINCT country_code
                         FROM profiles''')
    codes = []
    for row in data:
        codes.append(row[0])

    return codes


def get_profile_by_id(profile_id: int) -> Profile | None:
    data = read_query('''SELECT id, ip_address, country_code FROM profiles WHERE id = ?''',
                      (profile_id,)
                      )
    if not data:
        return None

    return Profile.from_query_result(*data[0])


def get_favourite_categories(profile_id: int) -> list[FavouriteCategory]:
    data = read_query('''SELECT c.id, c.name, i.relevance FROM interests i JOIN categories c ON i.category_id = c.id WHERE i.profile_id = ? ORDER BY i.relevance DESC''',
                      (profile_id, )
                      )

    categories = []
    for row in data:
        categories.append(FavouriteCategory.from_query_result(*row))

    return categories


def get_extended_profile(profile_id: int) -> ExtendedProfile | None:
    profile = get_profile_by_id(profile_id)
    if profile is None:
        return None
    favorite_categories = get_favourite_categories(profile_id)

    return ExtendedProfile(profile=profile, categories=favorite_categories)

def get_profile_id_by_ip_address(ip_address: str) -> int | None:
    data = read_query('''SELECT id FROM profiles WHERE ip_address = ?''',
                      (ip_address,)
                      )
    if not data:
        return None

    return data[0][0]