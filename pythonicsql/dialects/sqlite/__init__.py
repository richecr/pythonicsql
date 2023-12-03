from pythonicsql.dialects.client import Client


class SQLite(Client):
    def __init__(self, dialect: str, uri: str) -> None:
        super().__init__(dialect, uri)
