from typing import List
import unittest

from databases.core import Database
from pythonicsql.query.model.simple_attributes import SimpleAttributes
from pythonicsql.query.model.statement import Statements
from pythonicsql.query.query_builder import QueryBuilder

from pythonicsql.query.query_compiler import QueryCompiler

db = Database("sqlite:///example_test.db")


class TestQueryBuilder(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.query_compiler = QueryCompiler(db)
        self.query_builder = QueryBuilder(self.query_compiler)

    def test_clausare_select_params_success(self):
        sttms = self.query_builder.select(["id", "name"]).from_("users")._statements
        self._extracted_from_test_clausare_select_all_params_success(
            sttms, "id, name", "select id, name from users"
        )

    def test_clausare_select_all_params_success(self):
        sttms = self.query_builder.select().from_("users")._statements
        self._extracted_from_test_clausare_select_all_params_success(
            sttms, "*", "select * from users"
        )

    def _extracted_from_test_clausare_select_all_params_success(
        self, sttms: List[Statements], arg1: str, arg2: str
    ):
        self.assertEqual(sttms[0].type, "select")
        self.assertEqual(sttms[0].grouping, "columns")
        self.assertEqual(sttms[0].value, arg1)
        self.assertEqual(self.query_builder.to_sql(), arg2)

    def test_clausare_where_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where("name", "Test", "=")
            .where("id", "1")
            ._statements
        )
        sql = "select * from users where name = 'Test' and id = '1'"
        self.assert_sttm(
            sttms[-1], "where_operator", "where", "id", "1", "=", " and", sql
        )

    def test_clausare_or_where_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where("name", "Test", "=")
            .or_where("name", "Test 1", "=")
            ._statements
        )
        sql = "select * from users where name = 'Test' or name = 'Test 1'"
        self.assert_sttm(
            sttms[-1], "where_operator", "where", "name", "Test 1", "=", " or", sql
        )

    def test_clausare_where_in_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where_in("id", ["1", "2"])
            .where_in("id", ["3", "4"])
            ._statements
        )
        sql = "select * from users where id in ('1', '2') and id in ('3', '4')"
        self.assert_sttm(
            sttms[-1], "where_in", "where", "id", ["3", "4"], "in", " and", sql
        )

    def test_clausare_or_where_in_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where_in("id", ["1", "2"])
            .or_where_in("id", ["3", "4"])
            ._statements
        )
        sql = "select * from users where id in ('1', '2') or id in ('3', '4')"
        self.assert_sttm(
            sttms[-1], "where_in", "where", "id", ["3", "4"], "in", " or", sql
        )

    def test_clausare_where_like_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where("id", "3")
            .where_like("name", "%tes%")
            ._statements
        )
        sql = "select * from users where id = '3' and name like '%tes%'"
        self.assert_sttm(
            sttms[-1], "where_like", "where", "name", "%tes%", "like", " and", sql
        )

    def test_clausare_or_where_like_success(self):
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where("id", "3")
            .or_where_like("name", "%tes%")
            ._statements
        )
        sql = "select * from users where id = '3' or name like '%tes%'"
        self.assert_sttm(
            sttms[-1], "where_like", "where", "name", "%tes%", "like", " or", sql
        )

    def assert_sttm(
        self,
        sttm: Statements,
        type: str,
        grouping: str,
        column: str,
        value: str,
        operator: str,
        condition: str,
        sql: str,
    ):
        self.assertEqual(sttm.type, type)
        self.assertEqual(sttm.grouping, grouping)
        self.assertEqual(sttm.column, column)
        self.assertEqual(sttm.value, value)
        self.assertEqual(sttm.operator, operator)
        self.assertEqual(sttm.condition, condition)
        self.assertEqual(self.query_builder.to_sql(), sql)

    def test_clausare_limit_success(self):
        self.query_builder.select().from_("users").limit(10)
        self._extracted_from_test_clausare_limit("select * from users limit 10")

    def test_clausare_offset_success(self):
        self.query_builder.select().from_("users").limit(10).offset(1)
        self._extracted_from_test_clausare_limit(
            "select * from users limit 10 offset 1"
        )
        self.assertEqual(self.query_builder._simple.offset, 1)

    def _extracted_from_test_clausare_limit(self, sql):
        self.assertEqual(sql, self.query_builder.to_sql())
        self.assertEqual(self.query_builder._simple.limit, 10)

    async def test_clausare_exec_success(self):
        await db.execute("CREATE TABLE IF NOT EXISTS users (id int, name varchar);")
        sttms = (
            self.query_builder.select()
            .from_("users")
            .where("id", "3")
            .or_where_like("name", "%tes%")
            .limit(10)
            ._statements
        )
        sql = "select * from users where id = '3' or name like '%tes%' limit 10"
        self.assertEqual(sql, self.query_builder.to_sql())
        self.assertEqual(3, len(self.query_builder._statements))
        self.assertEqual(10, self.query_builder._simple.limit)
        await self.query_builder.exec()
        self.assertEqual(0, len(self.query_builder._statements))
        self.assertEqual(0, self.query_builder._simple.limit)


if __name__ == "__main__":
    unittest.main()
