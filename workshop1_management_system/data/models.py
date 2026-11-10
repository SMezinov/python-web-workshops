from pydantic import BaseModel


LEVELS = ('junior', 'mid', 'senior')


class Developer(BaseModel):
    id: int | None = None
    name: str
    level: str

    @classmethod
    def from_query_result(cls, id, name, level):
        return cls(id=id, name=name, level=LEVELS[level - 1])


class Project(BaseModel):
    id: int | None = None
    name: str
    status: str
    limit: int

    @classmethod
    def from_query_result(cls, id, name, is_open, team_limit):
        status = 'open' if is_open == 1 else 'closed'
        return cls(id=id, name=name, status=status, limit=team_limit)


class ProjectStatus(BaseModel):
    status: str
