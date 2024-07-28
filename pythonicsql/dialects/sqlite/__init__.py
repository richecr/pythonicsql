import sqlite3
from sqlite3 import Row
from typing import Any, Callable, Iterable, Optional, TypeVar

import aiosqlite

from pythonicsql.dialects.client import Client
from pythonicsql.query.model.database_config import Config

T = TypeVar("T")


class SQLite(Client):
    def __init__(self, dialect: str, config: Config) -> None:
        super().__init__(dialect, config)

    async def connect(self) -> None:
        uri = self.config.get("uri")
        if uri:
            self.db = await aiosqlite.connect(database=uri, detect_types=sqlite3.PARSE_DECLTYPES)
            self.set_row_factory(self.__dict_factory)
            return

        raise Exception("SQLite requires a URI")

    async def close(self) -> None:
        await self.db.close()

    async def execute(self, sql: str) -> Any:
        return await self.db.execute(sql)

    async def fetch(self, sql: str) -> Iterable[Row]:
        return await self.db.execute_fetchall(sql)

    async def fetch_one(self, sql: str) -> Optional[Row]:
        async with self.db.execute(sql) as cursor:
            return await cursor.fetchone()

    def set_row_factory(self, fn: Callable[[aiosqlite.Cursor, Row], Any]) -> None:
        self.db.row_factory = fn  # type: ignore

    def __dict_factory(self, cursor: aiosqlite.Cursor, row: Row) -> dict[str, Any]:
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}
