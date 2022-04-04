import psycopg2
import pytest
from dynaconf import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


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
