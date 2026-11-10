## Workshop - Project Management System

### 1. Project information
You are provided with a schema that stores information about Projects and Developers. Your task is to create a REST API that exposes functionality for interacting with that information.

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
- Schema:<br>
    ![Schema](images/devs_projects.png)

### 4. Models
- **Developer:**
   - `id`: int
   - `name`: str (unique)
   - `level`: str (allowed values: `'junior'`, `'mid'` or `'senior'`)
        - in the schema, **level** is INT column where 1 = junior, 2 = mid, 3 = senior
- **Project:**
   - `id`: int
   - `name`: str (unique)
   - `status`: str (allowed values: `'open'` or `'closed'`)
        - in the schema, related column is **is_open** where 1 = open, 0 = closed
   - `limit`: int
        - in the schema, related column is **team_limit** (because "limit" is keyword in SQL)
- Many developers can take part in many projects (depending on seniority level)

### 5. Endpoints

Use FastAPI to implement the required functionality. Try to design the endpoints to be as RESTful as possible

- use nouns in URLs
- use HTTP verbs for actions
- resource representations should be JSON

1. **Get all projects** - returns id, name, status, limit for all projects
    - option to filter by name - return projects that partially match provided name
    - option to filter by limit - return projects with limit less than or equal to provided limit
    - option to filter by open|closed status
2. **Get all devs** - returns id, name, level for all devs
    - option to filter by name - return devs that partially match provided name
    - option to filter by experience level - junior|mid|senior
3. **Get project by id**
    - returns id, name, status, limit for the project with provided ID
        - returns id, name, level for devs assigned to that project
4. **Get dev by id**
    - returns id, name, level for the dev with provided ID
        - returns id, name, status, limit for projects assigned to that dev
5. **Create project** - required data:
    - name: str - at least one symbol, unique
    - status: str - one of open|closed (note that value should be stored as int in db)
    - limit: int - positive integer 
6. **Create dev** - required data:
    - name: str - at least one symbol, unique
    - level: str - one of junior|mid|senior (note that value should be stored as int in db)
7. **Set project status**
    - sets a project status to open or closed
8. **Assign dev to project**
    - Cannot assign if project is in closed status.
    - Cannot assign if project limit is reached.
    - Only senior devs can be assigned to more than one project.
    - Each project should have at least one senior.
9. **Remove dev from project**
    - Do not check experience level when removing.

### 6. Deliverables
- zip archive of your solution
- preferably, a POSTMAN collection with the implemented endpoints (skip this if you use /docs for HTTP requests)