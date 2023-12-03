from pydantic import BaseModel


class SimpleAttributes(BaseModel):
    table_name: str | None = ""
    limit: int = 0
    offset: int = 0
    counter: int = 0
    is_dql: bool = False
