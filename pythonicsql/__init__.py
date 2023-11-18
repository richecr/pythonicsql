from pythonicsql.dialects.postgres import PostgresSQL
from pythonicsql.query.query_builder import QueryBuilder


class PythonicSQL:
    __slots__ = ["uri", "dialect", "client"]

    def __init__(self, config: dict) -> None:
        self.uri = config.get("uri")
        self.dialect = config.get("dialect")
        self.client = self._get_client()

    def _get_client(self) -> QueryBuilder:
        if self.dialect == "pg":
            return PostgresSQL(self.dialect, self.uri).builder

        raise Exception("Dialect not found")
