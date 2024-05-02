from pythonicsql.query.query_builder import QueryBuilder
from pythonicsql.query.query_compiler import QueryCompiler


class Client:
    __slots__ = ["dialect", "compiler", "builder"]

    def __init__(self, dialect: str) -> None:
        self.dialect = dialect
        self.compiler = QueryCompiler()
        self.builder = QueryBuilder(self.compiler)
