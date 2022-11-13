from functools import cached_property

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wire_service.settings import settings


class _DbConnection:
    @cached_property
    def engine(self):
        return create_engine(settings.DB_PATH, echo=settings.ECHO_SQL, future=True)

    @cached_property
    def Session(self):
        return sessionmaker(self.engine)


DbConnection = _DbConnection()
