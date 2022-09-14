import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from wire_service.db_model import Base
from wire_service.db_model.connection import DbConnection
from wire_service.settings import settings


def pytest_addoption(parser):
    parser.addoption(
        "--online",
        action="store_true",
        default=False,
        help="custom option: test with online postgres DB",
    )


@pytest.fixture(scope="session", autouse=True)
def set_test_settings(request):  #
    if request.config.getoption("--online", default=False):
        settings.configure(FORCE_ENV_FOR_DYNACONF="testing")
    else:
        settings.configure(FORCE_ENV_FOR_DYNACONF="sqlite_testing")


@pytest.fixture(scope="session", autouse=True)
def ensure_db_exists(set_test_settings):
    if settings.FORCE_ENV_FOR_DYNACONF != "sqlite_testing":
        con = psycopg2.connect(
            f"dbname='postgres' user='{settings.DB_USER}' host='{settings.DB_HOST}' port={settings.DB_PORT} password='{settings.DB_PASS}'"
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
