import unittest

from pythonicsql import PythonicSQL
from pythonicsql.dialects.postgres import PostgresSQL
from pythonicsql.dialects.sqlite import SQLite
from pythonicsql.query.exceptions.dialect_not_found import DialectNotFound
from pythonicsql.query.query_builder import QueryBuilder
from pythonicsql.query.query_compiler import QueryCompiler


class TestQueryBuilder(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.pythonicsql_sqlite = PythonicSQL(
            {"client": "sqlite", "config": {"uri": "sqlite+aiosqlite:///example.db"}}
        )
        self.pythonicsql_pg = PythonicSQL(
            {"client": "pg", "config": {"uri": "sqlite+aiosqlite:///example.db"}}
        )

    def test_pythonic_sqlite(self):
        self.assertIsInstance(self.pythonicsql_sqlite.client, SQLite)

    def test_pythonic_pg(self):
        self.assertIsInstance(self.pythonicsql_pg.client, PostgresSQL)

    def test_pythonic_dialect_not_found_exception(self):
        with self.assertRaises(DialectNotFound):
            self.pythonicsql_pg = PythonicSQL(
                {
                    "client": "sqllite",
                    "config": {"uri": "sqlite+aiosqlite:///example.db"},
                }
            )

    async def test_pythonic_connect(self):
        await self.pythonicsql_sqlite.client.connect()

    async def test_pythonic_disconnect(self):
        await self.pythonicsql_sqlite.client.disconnect()


if __name__ == "__main__":
    unittest.main()
