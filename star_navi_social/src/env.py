import os

from dotenv import load_dotenv


class Env:
    def __init__(self) -> None:
        load_dotenv()
        self._pg_user: str = os.environ["PG_USER"]
        self._pg_host: str = os.environ["PG_HOST"]
        self._pg_port: str = os.environ["PG_PORT"]
        self._pg_password: str = os.environ["PG_PASSWORD"]
        self._pg_db_name: str = os.environ["PG_DB_NAME"]

    @property
    def pg_db_name(self) -> str:
        return self._pg_db_name

    @property
    def pg_user(self) -> str:
        return self._pg_user

    @property
    def pg_host(self) -> str:
        return self._pg_host

    @property
    def pg_port(self) -> str:
        return self._pg_port

    @property
    def pg_password(self) -> str:
        return self._pg_password

    @property
    def db_url(self) -> str:
        return (
            "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
                username=self.pg_user,
                password=self.pg_password,
                host=self.pg_host,
                port=self.pg_port,
                db_name=self.pg_db_name,
            )
        )
