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

        cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            is_open INTEGER NOT NULL,
            team_limit INTEGER NOT NULL
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS devs (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            level INTEGER NOT NULL
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS devs_projects (
            dev_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            PRIMARY KEY (dev_id, project_id),
            FOREIGN KEY (dev_id) REFERENCES devs (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        );''')

    # data seed
    if query_count('SELECT COUNT(*) FROM projects;') == 0:
        print('Inserting projects')
        insert_query('''INSERT INTO projects (name, is_open, team_limit)
VALUES ('React Client Application', 1, 4),
       ('Payment System API', 0, 5),
       ('Tech Support Initiative', 1, 8);''')

    if query_count('SELECT COUNT(*) FROM devs;') == 0:
        print('Inserting devs')
        insert_query('''INSERT INTO devs (name, level)
VALUES ('Gosho Petrov', 2),
       ('Petar Georgiev', 1),
       ('Stamat Todorov', 3);''')

    if query_count('SELECT COUNT(*) FROM devs_projects;') == 0:
        print('Inserting devs into projects')
        insert_query('''INSERT INTO devs_projects (dev_id, project_id)
VALUES (1, 2),
       (2, 2),
       (3, 2),
       (3, 1);''')
