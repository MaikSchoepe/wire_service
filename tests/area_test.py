from dynaconf import settings


def test():
    assert settings.DB_NAME == "wiring_unittest"
