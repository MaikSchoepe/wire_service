from dynaconf import Dynaconf

settings = Dynaconf(settings_file=["settings.toml", ".secrets.toml"], environments=True)
