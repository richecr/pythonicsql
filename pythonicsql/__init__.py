__version__ = "0.1.0.dev1"

from typing import TypeVar

from pythonicsql.dialects.postgres import PostgresSQL
from pythonicsql.dialects.sqlite import SQLite
from pythonicsql.query.exceptions.dialect_not_found import DialectNotFound
from pythonicsql.query.model.database_config import DatabaseConfiguration
from pythonicsql.query.query_builder import QueryBuilder

T = TypeVar("T")


class PythonicSQL:
    __slots__ = ["dialect", "config", "client", "query"]

    def __init__(self, config: DatabaseConfiguration) -> None:
        self.config = config["config"]
        self.dialect = config["dialect"]
        self.client = self._get_client()
        self.query = self._query_builder()

    def _get_client(self) -> PostgresSQL | SQLite:
        if self.dialect == "pg":
            return PostgresSQL(self.dialect, self.config)
        elif self.dialect == "sqlite":
            return SQLite(self.dialect, self.config)

        raise DialectNotFound("Dialect not found")

    def _query_builder(self) -> QueryBuilder:
        return self.client.builder
