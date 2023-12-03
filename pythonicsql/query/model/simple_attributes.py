from dataclasses import dataclass

from pythonicsql.query.model.raw import Raw


@dataclass
class SimpleAttributes:
    table_name: str | None = ""
    limit: int = 0
    offset: int = 0
    counter: int = 0
    is_dql: bool = False
    raw: Raw | None = None
