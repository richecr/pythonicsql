from databases import Database

from pythonicsql.query.query_builder import QueryBuilder
from pythonicsql.query.query_compiler import QueryCompiler


class Client:
    __slots__ = ["uri", "dialect", "database", "compiler", "builder"]

    def __init__(self, dialect: str, uri: str) -> None:
        self.uri = uri
        self.dialect = dialect
        self.database = Database(self.uri)
        self.compiler = QueryCompiler(self.database)
        self.builder = QueryBuilder(self.compiler)
