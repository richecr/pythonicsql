import unittest

from pythonicsql import PythonicSQL
from pythonicsql.dialects.postgres import PostgresSQL
from pythonicsql.dialects.sqlite import SQLite
from pythonicsql.query.exceptions.dialect_not_found import DialectNotFound


class TestQueryBuilder(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.pythonicsql_sqlite = PythonicSQL({"dialect": "sqlite"})
        self.pythonicsql_pg = PythonicSQL({"dialect": "pg"})

    def test_pythonic_sqlite(self):
        self.assertIsInstance(self.pythonicsql_sqlite.client, SQLite)

    def test_pythonic_pg(self):
        self.assertIsInstance(self.pythonicsql_pg.client, PostgresSQL)

    def test_pythonic_dialect_not_found_exception(self):
        with self.assertRaises(DialectNotFound):
            self.pythonicsql_pg = PythonicSQL({"dialect": "sqllite"})


if __name__ == "__main__":
    unittest.main()
