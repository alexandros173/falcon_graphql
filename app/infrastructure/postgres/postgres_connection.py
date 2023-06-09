from contextlib import contextmanager

from config.general import Config

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session


class PostgresConnection:
    _engine = None

    def __init__(self, config: Config):
        params = config.POSTGRES

        self._conn_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
            params['user'],
            params['password'],
            params['host'],
            params['port'],
            params['db'],
        )

    def get_engine(self) -> Engine:
        if PostgresConnection.is_closed():
            PostgresConnection._engine = create_engine(self._conn_string, pool_size=2, max_overflow=1)

        return PostgresConnection._engine

    @contextmanager
    def get_session(self):
        session = Session(self.get_engine(), future=True)
        try:
            yield session
        finally:
            session.close()

    @classmethod
    def close(cls) -> None:
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None

    @classmethod
    def is_closed(cls) -> bool:
        return cls._engine is None
