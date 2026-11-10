from sqlite3 import connect

_DB_FILE = './data/dbfile.db'


def read_query(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0


def query_count(sql: str, sql_params=()):
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.fetchone()[0]


def init_database():
    # Create tables
    with connect(_DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                            id integer NOT NULL PRIMARY KEY,
                            ip_address text NOT NULL UNIQUE,
                            country_code text NOT NULL);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                            id integer NOT NULL PRIMARY KEY,
                            name text NOT NULL UNIQUE);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS interests (
                            category_id integer NOT NULL,
                            profile_id integer NOT NULL,
                            relevance integer NOT NULL,
                            PRIMARY KEY (category_id, profile_id),
                            FOREIGN KEY (category_id) REFERENCES categories (id),
                            FOREIGN KEY (profile_id) REFERENCES profiles (id));''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id integer NOT NULL PRIMARY KEY,
                            name text NOT NULL UNIQUE,
                            price real NOT NULL,
                            category_id integer NOT NULL,
                            FOREIGN KEY (category_id) REFERENCES categories (id));''')

    # data seed
    if query_count('SELECT COUNT(*) from categories') == 0:
        print('Inserting categories')
        insert_query('''INSERT INTO categories(name) VALUES 
                        ('Cell Phones'),
                        ('Computers and Accessories'),
                        ('Television');''')

    if query_count('SELECT COUNT(*) from products') == 0:
        print('Inserting products')
        insert_query('''INSERT INTO products(name, price, category_id) VALUES 
                        ('TV LCD 40 Inch',749.99,3),
                        ('Laptop',699.99,2),
                        ('Smartphone',1349.9,1),
                        ('Keyboard',99,2),
                        ('Improved Generic TV',239.5,3),
                        ('Turbo Smartphone v2',719,1),
                        ('Headphones',39,2)''')

    if query_count('SELECT COUNT(*) from profiles') == 0:
        print('Inserting profiles')
        insert_query('''INSERT INTO profiles(ip_address, country_code) VALUES 
                        ('81.161.239.88','BG'),
                        ('81.161.252.171','BG'),
                        ('104.123.59.151','SWE')''')

    if query_count('SELECT COUNT(*) from interests') == 0:
        print('Inserting interests')
        insert_query('''INSERT INTO interests(category_id, profile_id, relevance) VALUES 
                        (1,2,17),
                        (2,2,11),
                        (1,3,4),
                        (2,3,8),
                        (3,3,1),
                        (1,1,12)''')
