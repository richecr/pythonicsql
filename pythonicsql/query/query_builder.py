from typing import List
from pythonicsql.query.query_compiler import QueryCompiler
from pythonicsql.query.simple_attributes import SimpleAttributes
from pythonicsql.query.statement import Statements


class QueryBuilder:
    __slots__ = ["compiler", "_simple", "_statements", "components", "client"]

    def __init__(self, compiler: QueryCompiler) -> None:
        self.compiler = compiler
        self._simple: SimpleAttributes = SimpleAttributes()
        self._statements: List[Statements] = []

    def to_sql(self):
        self.compiler.set_options_builder(self._statements, self._simple)
        return self.compiler.to_sql()

    def select(self, columns: List[str]):
        self._statements.append(
            Statements(
                type="select",
                value=", ".join(columns),
                grouping="columns",
            )
        )
        return self

    def set_table_name(self, table_name: str):
        self._simple.table_name = table_name
        return self

    def from_(self, tn: str):
        return self.set_table_name(tn)

    def into(self, tn: str):
        return self.set_table_name(tn)

    def limit(self, limit_: int):
        self._simple.limit = limit_
        return self

    async def exec(self):
        self.compiler.set_options_builder(self._statements, self._simple)
        return await self.compiler.exec()
