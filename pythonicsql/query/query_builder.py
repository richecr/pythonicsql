from typing import Any, List

from pythonicsql.query.model.raw import Raw
from pythonicsql.query.model.statement import Statements
from pythonicsql.query.model.simple_attributes import SimpleAttributes
from pythonicsql.query.query_compiler import QueryCompiler


class QueryBuilder:
    __slots__ = ["compiler", "_simple", "_statements", "components", "client"]

    def __init__(self, compiler: QueryCompiler) -> None:
        self.compiler = compiler
        self._simple: SimpleAttributes = SimpleAttributes()
        self._statements: List[Statements] = []

    def to_sql(self):
        self.compiler.set_options_builder(self._statements, self._simple)
        sql = self._simple.raw.sql if self._simple.raw else self.compiler.to_sql()
        return sql

    def select(self, columns: List[str] | None = "*"):
        value = ", ".join(columns) if columns else "*"
        self._statements.append(
            Statements(
                type="select",
                grouping="columns",
                value=value,
            )
        )
        return self

    def set_table_name(self, table_name: str):
        self._simple.table_name = table_name
        return self

    def from_(self, tn: str):
        return self.set_table_name(tn)

    def _where(
        self,
        type: str,
        column: str,
        value: List | str | int | Any,
        condition: str = " and",
        operator: str = " = ",
    ):
        self._statements.append(
            Statements(
                type=type,
                grouping="where",
                value=value,
                column=column,
                condition=condition,
                operator=operator,
            )
        )

    def where(self, column: str, value: Any, operator: str = "="):
        self._where(
            type="where_operator", column=column, value=value, operator=operator
        )
        return self

    def or_where(self, column: str, value: Any, operator: str = "="):
        self._where(
            type="where_operator",
            column=column,
            value=value,
            operator=operator,
            condition=" or",
        )
        return self

    def where_in(self, column: str, values: List):
        self._where(type="where_in", column=column, value=values, operator="in")
        return self

    def or_where_in(self, column: str, values: List):
        self._where("where_in", column, values, " or", "in")
        return self

    def where_like(self, column: str, value: str):
        self._where("where_like", column, value, " and", "like")
        return self

    def or_where_like(self, column: str, value: str):
        self._where("where_like", column, value, " or", "like")
        return self

    def limit(self, limit_: int):
        self._simple.limit = limit_
        return self

    def offset(self, offset: int):
        self._simple.offset = offset
        return self

    async def exec(self):
        self.compiler.set_options_builder(self._statements, self._simple)
        result = await self.compiler.exec()
        self.reset()
        return result

    def raw(self, sql: str):
        self._simple.is_dql = sql.lower().startswith("select")
        self._simple.raw = Raw(sql)
        return self

    def reset(self):
        self._statements = []
        self._simple = SimpleAttributes()
