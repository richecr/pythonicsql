import unittest

from databases.core import Database

from pythonicsql.query.model.simple_attributes import SimpleAttributes
from pythonicsql.query.model.statement import Statements
from pythonicsql.query.query_compiler import QueryCompiler

db = Database("sqlite:///example_test.db")


class TestQueryCompiler(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.query_compiler = QueryCompiler(db)
        self.query_compiler._simple = SimpleAttributes(table_name="users")

    def test_columns_success(self):
        self.query_compiler._statements = [
            Statements(type="select", value="id, name", grouping="columns"),
            Statements(
                type="where_operator",
                column="id",
                value="1",
                operator="=",
                grouping="where",
            ),
        ]
        sql = self.query_compiler.to_sql()
        self.assertEqual(sql, "select id, name from users where id = '1'")

    def test_clausare_where_operator_success(self):
        self.query_compiler._statements = [
            Statements(type="select", value="id, name", grouping="columns"),
            Statements(
                type="where_operator",
                column="id",
                value="1",
                operator="=",
                grouping="where",
            ),
            Statements(
                type="where_in",
                column="id",
                value=["1", "2", "3"],
                grouping="where",
            ),
        ]
        sql = self.query_compiler.to_sql()
        self.assertEqual(
            sql, "select id, name from users where id = '1' and id in ('1', '2', '3')"
        )

    def test_clausare_or_where_operator_success(self):
        self.query_compiler._statements = [
            Statements(type="select", value="id, name", grouping="columns"),
            Statements(
                type="where_in",
                column="id",
                value=["1", "2", "3"],
                grouping="where",
            ),
            Statements(
                type="where_operator",
                column="id",
                value="1",
                operator="=",
                condition=" or",
                grouping="where",
            ),
        ]
        sql = self.query_compiler.to_sql()
        self.assertEqual(
            sql,
            "select id, name from users where id in ('1', '2', '3') or id = '1'",
        )

    def test_clausare_and_where_in_success(self):
        self._extracted_from_test_clausare_where_in_success(
            "name",
            "Test",
            " and",
            "select * from users where name = 'Test' and id in ('1', '2', '3')",
        )

    def test_clausare_or_where_in_success(self):
        self._extracted_from_test_clausare_where_in_success(
            "id",
            "1",
            " or",
            "select * from users where id = '1' or id in ('1', '2', '3')",
        )

    def _extracted_from_test_clausare_where_in_success(
        self, column, value, condition, expect
    ):
        self.query_compiler._statements = [
            Statements(type="select", value="*", grouping="columns"),
            Statements(
                type="where_operator",
                column=column,
                value=value,
                operator="=",
                grouping="where",
            ),
            Statements(
                type="where_in",
                column="id",
                value=["1", "2", "3"],
                condition=condition,
                grouping="where",
            ),
        ]
        sql = self.query_compiler.to_sql()
        self.assertEqual(sql, expect)

    def test_clausare_and_where_like_success(self):
        self._extracted_from_test_clausare_where_like_success(
            " and",
            "select * from users where id = '1' and name like '%li%'",
        )

    def test_clausare_or_where_like_success(self):
        self._extracted_from_test_clausare_where_like_success(
            " or",
            "select * from users where id = '1' or name like '%li%'",
        )

    def _extracted_from_test_clausare_where_like_success(self, condition, expect):
        self.query_compiler._statements = [
            Statements(type="select", value="*", grouping="columns"),
            Statements(
                type="where_operator",
                column="id",
                value="1",
                operator="=",
                grouping="where",
            ),
            Statements(
                type="where_like",
                column="name",
                value="%li%",
                condition=condition,
                grouping="where",
            ),
        ]
        sql = self.query_compiler.to_sql()
        self.assertEqual(sql, expect)

    def test_set_options_builder_success(self):
        self.query_compiler.set_options_builder(
            [
                Statements(type="select", value="id, name", grouping="columns"),
                Statements(
                    type="where_operator",
                    column="id",
                    value="1",
                    operator="=",
                    grouping="where",
                ),
            ],
            SimpleAttributes(table_name="users", is_dql=True),
        )
        sql = self.query_compiler.to_sql()
        self.assertEqual(sql, "select id, name from users where id = '1'")

    async def test_exec_success(self):
        await db.execute("CREATE TABLE IF NOT EXISTS users (id int, name varchar);")
        self.query_compiler.set_options_builder(
            [
                Statements(type="select", value="id, name", grouping="columns"),
                Statements(
                    type="where_operator",
                    column="id",
                    value="1",
                    operator="=",
                    grouping="where",
                ),
            ],
            SimpleAttributes(table_name="users", is_dql=True),
        )
        sql = self.query_compiler.to_sql()
        await self.query_compiler.exec()
        self.assertEqual(sql, "select id, name from users where id = '1'")

    def test_offset_success(self):
        self.query_compiler._statements = [
            Statements(type="select", value="id, name", grouping="columns"),
        ]
        self.query_compiler._simple = SimpleAttributes(
            table_name="users", limit=100, offset=10
        )
        sql = self.query_compiler.to_sql()
        self.assertEqual(sql, "select id, name from users limit 100 offset 10")


if __name__ == "__main__":
    unittest.main()
