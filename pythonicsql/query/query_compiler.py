from collections import defaultdict
from typing import Any, Dict, List, Union

from pythonicsql.query.model.simple_attributes import SimpleAttributes
from pythonicsql.query.model.statement import Statements


class QueryCompiler:
    __slots__ = ["_simple", "_statements", "groups_dict"]

    _simple: SimpleAttributes
    _statements: Dict[str, Union[List[Statements], Statements]]
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

    def __init__(self) -> None:
        self.groups_dict: dict[str, List[Statements]] = defaultdict(list)

    def to_sql(self) -> str:
        first_statements = []
        end_statements = []

        # TODO: Fix self._statements does not have the limit or offset
        for component in self._statements:
            if statement := getattr(self, component, lambda _: None)(
                self._statements[component]
            ):
                match component:
                    case "comments" | "columns" | "join" | "where" | "limit":
                        first_statements.append(statement)
                    case _:
                        end_statements.append(statement)
        return " ".join(first_statements + end_statements)

    def columns(self, statement: Statements) -> str:
        self._simple.is_dql = True
        table_name = self._simple.table_name
        fields = statement.value
        return f"select {fields} from {table_name}"

    def where(self, statements: List[Statements]) -> str:
        sql: List[str] = []
        for clausare_where in statements:
            stmt = self[clausare_where.type](clausare_where)
            if not sql:
                sql.append(stmt)
            else:
                sql.extend((clausare_where.condition, stmt))
        return "where" + "".join(sql)

    def where_operator(self, statement: Statements) -> str:
        return " {column} {operator} '{values}'".format(
            column=statement.column, operator=statement.operator, values=statement.value
        )

    def where_in(self, statement: Statements) -> str:
        values = ", ".join(f"'{v}'" for v in statement.value)
        return " {column} in ({values})".format(column=statement.column, values=values)

    def where_like(self, statement: Statements) -> str:
        return " {column} like '{value}'".format(
            column=statement.column, value=statement.value
        )

    def limit(self) -> str:
        print("AAAAAAAA")
        return (
            f"limit {self._simple.limit}"
            if self._simple.limit and self._simple.limit > 0
            else ""
        )

    def offset(self) -> str:
        return (
            f"offset {self._simple.offset}"
            if self._simple.offset and self._simple.offset > 0
            else ""
        )

    def set_options_builder(
        self,
        statements: Dict[str, Union[List[Statements], Statements]],
        simple: SimpleAttributes,
    ) -> None:
        self._statements = statements
        self._simple = simple

    def reset(self) -> None:
        self.groups_dict = defaultdict(list)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
