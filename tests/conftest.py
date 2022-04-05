import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from wire_service.db_model import Base
from wire_service.db_model.connection import DbConnection
from wire_service.settings import settings


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope="session", autouse=True)
def ensure_db_exists(set_test_settings):
    con = psycopg2.connect(
        f"dbname='postgres' user='{settings.DB_USER}' host='{settings.DB_HOST}' password='{settings.DB_PASS}'"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = con.cursor()

    cursor.execute(
        f"select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{settings.DB_NAME}'));"
    )
    exists = cursor.fetchone()[0]

    if not exists:
        cursor.execute(f"CREATE DATABASE {settings.DB_NAME};")

    con.close()

    Base.metadata.drop_all(DbConnection.engine)
    Base.metadata.create_all(DbConnection.engine)
