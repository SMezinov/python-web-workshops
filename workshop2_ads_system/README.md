## Workshop - Ad Service

### 1. Project information
You are provided with a schema that stores information about Products, Profiles, Interests and Categories. Your task is to create a REST API that exposes functionality for interacting with that information.

### 2. Goals
- Practice writing SQL queries
- Practice using FastAPI
- Practice designing RESTful endpoints

### 3. Database
- The database in use is SQLite.
    - All the information will be stored locally in `/data/dbfile.db`.
    - SQL syntax is identical to MariaDB for the purposes of this workshop.
- On application startup, the `init_database` function will create the database schema and will populate it with data.
- You are allowed to change the data (obviously), but **DO NOT ALTER** the schema (no new tables or columns).
- Schema:  
    ![Schema](images/ad_service_db.png)

### 4. Models
- **Profile** - represents an anonymous internet user.
    - `id`: int
    - `ip_address`: str 
    - `country_code`: str 
- **Category** - represents a category of advertised products.
    - `id`: int
    - `name`: str
- **Interest** - represents the level of interest that a **Profile** expresses towards a **Category**. Higher `relevance` value = higher interest.
    - `profile_id`: int
    - `category_id`: int
    - `relevance`: int
- **Product** - represents an advertised product. A product can be part of only one category.
    - `id`: int
    - `name`: str
    - `price`: float
    - `category_id`: int

### 5. Endpoints

Use FastAPI to implement the required functionality. Try to design the endpoints to be as RESTful as possible

- use nouns in URLs
- use HTTP verbs for actions
- resource representations should be JSON

1. **Get all profiles** 
    - accepts optional `country_code` query parameter
    - returns JSON list with profiles, containing `id`, `ip_address`, and `country_code`
    - option to filter by `country_code`
2. **Get all country codes**
    - returns JSON list of all unique `country_code`s present in the database
3. **Get profile by id** 
    - accepts `profile_id` path parameter
    - returns JSON containing the profile `id`, `ip_address`, and `country_code`
        - also includes list of favourite categories (`id`, `name`, `relevance`) sorted by `relevance` in decreasing order
4. **View product** 
    - accepts `profile_id` and `product_id` as path parameters
    - should increase the profile's interest relevance for that product category by 5% (rounded up)
    - should create new profile interest for that category, if not present - initial relevance 1
5. **Serve ad**
    - accepts `ip_address` as path parameter
    - returns JSON representing `id`, `name`, `price` of one **random** product
        - option #1: passed `ip_address` has interests - random product is selected from top 3 interests
        - option #2: no associated interests - return any random product from any category
6. **Get categories** 
    - optional `country_code` query parameter
    - returns JSON lists of categories - `id`, `name`, and `cumulative_relevance` 
        - `cumulative_relevance` is the sum of all interests' relevance for that category
    - option to filter top categories for `country_code`
        - `cumulative_relevance` must be calculated only from `interests` that are associated with profiles having the `country_code`
    - displayed in decreasing order by `cumulative_relevance`

### 6. Deliverables
- zip archive of your solution
- preferably, a POSTMAN collection with the implemented endpoints (skip this if you use /docs for HTTP requests)
