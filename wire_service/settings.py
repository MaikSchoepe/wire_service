import json

from dynaconf import Dynaconf

settings = Dynaconf(settings_file=["settings.toml", ".secrets.toml"], environments=True)


def load_cable_types() -> dict:
    with open("./config/cable_types.json") as f:
        return json.load(f)
