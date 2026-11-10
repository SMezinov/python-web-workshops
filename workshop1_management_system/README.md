Project Management System

Стартиране от папката на проекта:
`python -m uvicorn main:app --reload`

Заявките могат да се изпращат през http://127.0.0.1:8000/docs
SQLite базата е във файла `data/dbfile.db`

GET /projects  Незадължителни филтри: name, limit, status
GET /devs  Незадължителни филтри: name, level
GET /projects/{id}  Проект с неговите разработчици
GET /devs/{id}  Разработчик с неговите проекти
POST /projects  JSON с name, status и limit
POST /devs  JSON с name и level
PUT /projects/{id}/status  JSON със status
POST /projects/{project_id}/devs/{dev_id}  Назначаване без тяло
DELETE /projects/{project_id}/devs/{dev_id}  Премахване без тяло
