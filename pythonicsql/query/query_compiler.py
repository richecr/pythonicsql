from collections import defaultdict
from dataclasses import fields
from itertools import groupby
from typing import List

from databases import Database
from pythonicsql.query.simple_attributes import SimpleAttributes

from pythonicsql.query.statement import Statements


class QueryCompiler:
    __slots__ = ["_simple", "_statements", "client", "groups_dict"]

    _simple: SimpleAttributes
    _statements: List[Statements]
    components: List[str] = [
        "columns",
        # "join",
        # "where",
        # "union",
        # "group",
        # "having",
        # "order",
        "limit",
        # "offset",
    ]

    def __init__(self, client: Database) -> None:
        self.client = client
        self.groups_dict: dict[str, List[Statements]] = defaultdict(list)

    def to_sql(self):
        first_statements = []
        end_statements = []
        groups = groupby(self._statements, lambda x: x.grouping)
        for key, g in groups:
            self.groups_dict[key].extend(list(g))
        for component in self.components:
            statement = self[component]()
            match component:
                case "union":
                    pass
                case "comments" | "columns" | "join" | "where" | "limit":
                    first_statements.append(statement)
                case _:
                    end_statements.append(statement)
        return " ".join(first_statements)

    def columns(self):
        self._simple.is_dql = True
        columns = self.groups_dict["columns"]
        table_name = self._simple.table_name
        sql_ = "select {fields} from {table_name}"
        if len(columns) == 0:
            sql_ = sql_.format(fields="*", table_name=table_name)
        else:
            sql_ = sql_.format(fields=columns[0].value, table_name=table_name)
        return sql_

    def limit(self):
        sql = ""
        if self._simple.limit and self._simple.limit > 0:
            sql = " limit {}".format(self._simple.limit)
        return sql

    def set_options_builder(
        self, statements: List[Statements], simple: SimpleAttributes
    ):
        self._statements = statements
        self._simple = simple

    async def exec(self):
        result = None
        query = self.to_sql()
        print(query)
        if self._simple.is_dql:
            result = await self.client.fetch_all(query=query)
        else:
            result = await self.client.execute(query=query)

        return result

    def __getitem__(self, key):
        return getattr(self, key)
