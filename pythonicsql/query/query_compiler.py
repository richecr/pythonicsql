from collections import defaultdict
from itertools import groupby
from typing import List

from databases import Database

from pythonicsql.query.model.simple_attributes import SimpleAttributes
from pythonicsql.query.model.statement import Statements


class QueryCompiler:
    __slots__ = ["_simple", "_statements", "client", "groups_dict"]

    _simple: SimpleAttributes
    _statements: List[Statements]
    components: List[str] = [
        "columns",
        # "join",
        "where",
        "union",
        # "group",
        # "having",
        # "order",
        "limit",
        "offset",
    ]

    def __init__(self, client: Database) -> None:
        self.client = client
        self.groups_dict: dict[str, List[Statements]] = defaultdict(list)

    def to_sql(self):
        first_statements = []
        end_statements = []

        self.groups_dict = {
            key: list(group)
            for key, group in groupby(self._statements, lambda x: x.grouping)
        }
        for component in self.components:
            if statement := getattr(self, component, lambda: None)():
                match component:
                    case "comments" | "columns" | "join" | "where" | "limit":
                        first_statements.append(statement)
                    case _:
                        end_statements.append(statement)
        return " ".join(first_statements + end_statements)

    def columns(self):
        self._simple.is_dql = True
        if columns := self.groups_dict.get("columns"):
            table_name = self._simple.table_name
            sql_ = "select {fields} from {table_name}"
            return sql_.format(fields=columns[0].value, table_name=table_name)
        return ""

    def where(self):
        sql = []
        if wheres := self.groups_dict.get("where"):
            for clausare_where in wheres:
                stmt = self[clausare_where.type](clausare_where)
                if not sql:
                    sql.append(stmt)
                else:
                    sql.extend((clausare_where.condition, stmt))
            return "where" + "".join(sql)
        return ""

    def where_operator(self, statement: Statements):
        return " {column} {operator} '{values}'".format(
            column=statement.column, operator=statement.operator, values=statement.value
        )

    def where_in(self, statement: Statements):
        values = ", ".join(f"'{v}'" for v in statement.value)
        return " {column} in ({values})".format(column=statement.column, values=values)

    def where_like(self, statement: Statements):
        return " {column} like '{value}'".format(
            column=statement.column, value=statement.value
        )

    def limit(self):
        return (
            f"limit {self._simple.limit}"
            if self._simple.limit and self._simple.limit > 0
            else ""
        )

    def offset(self):
        return (
            f"offset {self._simple.offset}"
            if self._simple.offset and self._simple.offset > 0
            else ""
        )

    def set_options_builder(
        self, statements: List[Statements], simple: SimpleAttributes
    ):
        self._statements = statements
        self._simple = simple

    async def exec(self):
        query = self._simple.raw.sql if self._simple.raw else self.to_sql()
        self.reset()
        return (
            await self.client.fetch_all(query=query)
            if self._simple.is_dql
            else await self.client.execute(query=query)
        )

    def reset(self):
        self.groups_dict = defaultdict(list)

    def __getitem__(self, key):
        return getattr(self, key)
