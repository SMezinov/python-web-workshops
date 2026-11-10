from data.database import read_query
from data.models import Category


def get_top_categories(profile_id: int) -> list[int]:
    data = read_query('''SELECT category_id FROM interests WHERE profile_id = ? ORDER BY relevance DESC LIMIT 3''',
                      (profile_id, ))
    if not data:
        return []

    top_categories = []
    for row in data:
        top_categories.append(row[0])

    return top_categories

def get_all_categories(country_code: str | None = None) -> list[Category]:
    if country_code is not None:
        data = read_query('''SELECT c.id, c.name, COALESCE(SUM(CASE WHEN p.country_code = ? THEN i.relevance ELSE 0 END), 0) AS cumulative_relevance 
                             FROM categories c 
                                      LEFT JOIN interests i ON i.category_id = c.id 
                                      LEFT JOIN profiles p ON p.id = i.profile_id
                          GROUP BY c.id, c.name
                          ORDER BY cumulative_relevance DESC ''', (country_code,)
                          )
    else:
        data = read_query('''SELECT c.id, c.name,
                                   COALESCE(SUM(i.relevance), 0) AS cumulative_relevance
                            FROM categories c
                            LEFT JOIN interests i ON i.category_id = c.id
                            GROUP BY c.id, c.name
                            ORDER BY cumulative_relevance DESC''')

    categories = []
    for row in data:
        categories.append(Category.from_query_result(*row))

    return categories