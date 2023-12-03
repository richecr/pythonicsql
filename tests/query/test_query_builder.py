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


if __name__ == "__main__":
    unittest.main()
