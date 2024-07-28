from typing import Any, Iterable, List, Optional, TypeVar

from pythonicsql.query.model.database_config import Config
from pythonicsql.query.query_builder import QueryBuilder
from pythonicsql.query.query_compiler import QueryCompiler

T = TypeVar("T")


class Client:
    __slots__ = ["dialect", "config", "compiler", "builder"]

    def __init__(self, dialect: str, config: Config) -> None:
        self.config = config
        self.dialect = dialect
        self.compiler = QueryCompiler(self)
        self.builder = QueryBuilder(self.compiler)

    async def connect(self) -> None:
        raise Exception("Connect Method not implemented")

    async def close(self) -> None:
        raise Exception("Close Method not implemented")

    async def execute(self, sql: str) -> str | Any:
        raise Exception("Execute method not implemented")

    async def fetch(self, sql: str) -> List[Any] | Iterable[Any]:
        raise Exception("Fetch method not implemented")

    async def fetch_one(self, sql: str) -> Optional[Any]:
        raise Exception("Fetch one method not implemented")
