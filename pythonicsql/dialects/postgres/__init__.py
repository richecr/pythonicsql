from typing import Generic, List, TypeVar

import asyncpg

from pythonicsql.dialects.client import Client
from pythonicsql.query.model.database_config import Config


class PostgresSQL(Client):
    __slots__ = ["dialect", "db"]

    def __init__(self, dialect: str, config: Config) -> None:
        super().__init__(dialect, config)

    async def connect(self) -> None:
        uri = self.config.get("uri")
        if uri:
            self.db = await asyncpg.connect(dsn=uri)
            return

        self.db = await asyncpg.connect(
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            port=self.config["port"],
            host=self.config["host"],
            timeout=self.config["timeout"],
            ssl=self.config["ssl"],
        )

    async def close(self) -> None:
        await self.db.close()

    async def execute(self, sql: str) -> str:
        res = await self.db.execute(sql)
        return res

    async def fetch(self, sql: str) -> List[asyncpg.Record]:
        return await self.db.fetch(sql)

    async def fetch_one(self, sql: str) -> asyncpg.Record | None:
        return await self.db.fetchrow(sql)
