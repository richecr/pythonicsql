__version__ = "0.1.0.dev1"

from pythonicsql.dialects.client import Client
from pythonicsql.dialects.sqlite import SQLite
from pythonicsql.dialects.postgres import PostgresSQL

from pythonicsql.query.query_builder import QueryBuilder
from pythonicsql.query.model.database_config import DatabaseConfiguration
from pythonicsql.query.exceptions.dialect_not_found import DialectNotFound


class PythonicSQL:
    __slots__ = ["dialect", "client", "query"]

    def __init__(self, config: DatabaseConfiguration) -> None:
        self.dialect = config.get("dialect")
        self.client = self._get_client()
        self.query = self._query_builder()

    def _get_client(self) -> Client:
        if self.dialect == "pg":
            return PostgresSQL(self.dialect)
        elif self.dialect == "sqlite":
            return SQLite(self.dialect)

        raise DialectNotFound("Dialect not found")

    def _query_builder(self) -> QueryBuilder:
        return self.client.builder
