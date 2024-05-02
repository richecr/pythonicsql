from pythonicsql.dialects.client import Client


class PostgresSQL(Client):
    def __init__(self, dialect: str) -> None:
        super().__init__(dialect)
