from pythonicsql.dialects.client import Client


class SQLite(Client):
    def __init__(self, dialect: str) -> None:
        super().__init__(dialect)
